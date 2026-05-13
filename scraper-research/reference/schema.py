"""Data models + extractor protocol.

The three persistence shapes from ARCHITECTURE.md, expressed as Pydantic
v2 models:

  RawResponseRecord    — what we persist for every fetch attempt.
  ExtractionRecord     — what we persist when extraction succeeds.
  ExtractionFailure    — what we persist when extraction or detection fails.

Plus the ``Extractor`` protocol, with a ``ProductExtractor`` example
demonstrating per-record schema versioning.
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Protocol

from pydantic import BaseModel, Field, ValidationError, field_validator

from .detector import Classification
from .fetcher import RawResponse


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --------------------------------------------------------------------------- #
# Persistence shapes                                                          #
# --------------------------------------------------------------------------- #

class RawResponseRecord(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    run_id: uuid.UUID
    url: str
    url_hash: str
    method: str
    request_headers: Dict[str, str] = Field(default_factory=dict)
    request_body_hash: Optional[str] = None
    status_code: Optional[int]
    response_headers: Dict[str, str] = Field(default_factory=dict)
    body: bytes
    body_hash: str
    body_bytes: int
    content_type: Optional[str]
    fetched_at: datetime
    fetcher: str
    proxy_id: Optional[str]
    attempt: int
    duration_ms: int
    detection_flags: List[str] = Field(default_factory=list)
    classification: str

    @classmethod
    def from_raw(
        cls,
        raw: RawResponse,
        *,
        run_id: uuid.UUID,
        classification: Classification,
    ) -> "RawResponseRecord":
        return cls(
            run_id=run_id,
            url=raw.request.url,
            url_hash=_sha256(raw.request.url.encode("utf-8")),
            method=raw.request.method,
            request_headers=dict(raw.request.headers),
            request_body_hash=_sha256(raw.request.body) if raw.request.body else None,
            status_code=raw.status_code,
            response_headers=dict(raw.headers),
            body=raw.body,
            body_hash=_sha256(raw.body),
            body_bytes=len(raw.body),
            content_type=raw.headers.get("content-type") or raw.headers.get("Content-Type"),
            fetched_at=datetime.fromtimestamp(raw.fetched_at, tz=timezone.utc),
            fetcher=raw.fetcher,
            proxy_id=raw.proxy_id,
            attempt=raw.attempt,
            duration_ms=raw.duration_ms,
            detection_flags=classification.flags,
            classification=classification.severity,
        )


class ExtractionRecord(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    raw_response_id: uuid.UUID
    natural_key: str
    schema_version: int
    payload: Dict[str, Any]
    extracted_at: datetime = Field(default_factory=_utcnow)


class ExtractionFailure(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    raw_response_id: uuid.UUID
    reason: str  # missing_field / parse_error / blocked / captcha / soft_404 / schema_mismatch
    error_class: Optional[str] = None
    error_message: Optional[str] = None
    traceback: Optional[str] = None
    failed_at: datetime = Field(default_factory=_utcnow)
    resolved_at: Optional[datetime] = None


# --------------------------------------------------------------------------- #
# Extractor protocol                                                          #
# --------------------------------------------------------------------------- #

class ExtractionResult(BaseModel):
    """Container returned by extractors. Use one of `records` or `failure`."""

    records: List[ExtractionRecord] = Field(default_factory=list)
    failure: Optional[ExtractionFailure] = None


class Extractor(Protocol):
    schema_version: int

    def extract(self, raw_record: RawResponseRecord) -> ExtractionResult: ...


# --------------------------------------------------------------------------- #
# Example domain model + extractor                                            #
# --------------------------------------------------------------------------- #

class Product(BaseModel):
    """Per-record Pydantic model. Validation failures route to DLQ."""

    sku: str
    title: str
    price_cents: int
    currency: str = "USD"
    in_stock: bool

    @field_validator("currency")
    @classmethod
    def _currency_upper(cls, v: str) -> str:
        return v.upper()


class ProductExtractor:
    """Reference extractor: parse HTML → list of Products.

    The actual selector logic is intentionally minimal. Real extractors
    will use ``selectolax`` or ``parsel``; the contract — validate via
    Pydantic, route failures to ExtractionFailure, bump
    ``schema_version`` on breaking changes — is what matters.
    """

    schema_version = 1

    def extract(self, raw_record: RawResponseRecord) -> ExtractionResult:
        try:
            from selectolax.parser import HTMLParser  # lazy
        except ImportError as e:
            return ExtractionResult(
                failure=ExtractionFailure(
                    raw_response_id=raw_record.id,
                    reason="parse_error",
                    error_class="ImportError",
                    error_message=str(e),
                )
            )

        tree = HTMLParser(raw_record.body.decode("utf-8", errors="replace"))
        records: List[ExtractionRecord] = []
        for node in tree.css("[data-product-sku]"):
            try:
                price_text = (node.css_first(".price").text(strip=True) if node.css_first(".price") else "").lstrip("$")
                product = Product(
                    sku=node.attributes.get("data-product-sku", "").strip(),
                    title=(node.css_first(".title").text(strip=True) if node.css_first(".title") else ""),
                    price_cents=int(round(float(price_text) * 100)) if price_text else 0,
                    in_stock=node.attributes.get("data-in-stock", "false").lower() == "true",
                )
            except (ValidationError, ValueError, AttributeError) as e:
                # One bad node shouldn't kill the whole page; log and continue.
                # In production this would emit a metric + sample to logs.
                continue
            records.append(
                ExtractionRecord(
                    raw_response_id=raw_record.id,
                    natural_key=product.sku,
                    schema_version=self.schema_version,
                    payload=product.model_dump(),
                )
            )

        if not records:
            return ExtractionResult(
                failure=ExtractionFailure(
                    raw_response_id=raw_record.id,
                    reason="missing_field",
                    error_message="no [data-product-sku] nodes parsed",
                )
            )
        return ExtractionResult(records=records)


# --------------------------------------------------------------------------- #
# Storage protocol                                                            #
# --------------------------------------------------------------------------- #

class Storage(Protocol):
    def write_raw(self, record: RawResponseRecord) -> None: ...
    def write_extracted(self, records: List[ExtractionRecord]) -> None: ...
    def write_failure(self, failure: ExtractionFailure) -> None: ...


class InMemoryStorage:
    """Trivial sink, useful for tests and the example DAG."""

    def __init__(self):
        self.raw: List[RawResponseRecord] = []
        self.extracted: List[ExtractionRecord] = []
        self.failures: List[ExtractionFailure] = []

    def write_raw(self, record: RawResponseRecord) -> None:
        self.raw.append(record)

    def write_extracted(self, records: List[ExtractionRecord]) -> None:
        self.extracted.extend(records)

    def write_failure(self, failure: ExtractionFailure) -> None:
        self.failures.append(failure)
