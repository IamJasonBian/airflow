"""Orchestrator: wires fetcher + proxy + detectors + extractor + storage.

This is the only component that knows the *order* in which things
happen. Everything else is a protocol it calls. Adding a new fetcher /
proxy / detector / extractor never touches this file.

Run lifecycle:

    1. acquire a proxy lease for the URL's domain
    2. fetch
    3. classify (run all detectors)
    4. persist raw_response (always)
    5. report classification back to the proxy lease (for burn list)
    6. on retryable → backoff + retry (different proxy)
       on blocked   → escalate fetcher tier (caller-supplied)
       on dlq       → write extraction_failure, stop
       on ok        → extract, persist extracted / failure
"""

from __future__ import annotations

import logging
import random
import threading
import time
import traceback
import uuid
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Sequence
from urllib.parse import urlsplit

from .detector import Classification, Detector, classify
from .fetcher import Fetcher, RawResponse, Request
from .proxy import ProxyLease, ProxyProvider
from .schema import (
    ExtractionFailure,
    Extractor,
    RawResponseRecord,
    Storage,
)

log = logging.getLogger(__name__)


@dataclass
class ScrapeConfig:
    name: str
    fetcher: Fetcher
    proxy: ProxyProvider
    detectors: Sequence[Detector]
    extractor: Extractor
    storage: Storage
    max_attempts: int = 4
    base_backoff_s: float = 1.0
    max_backoff_s: float = 30.0
    rate_limit_per_host_per_s: float = 1.0
    # Called when a blocked classification is hit. Receives (request, attempt)
    # and returns a (Fetcher, ProxyProvider) tuple to use for the next try.
    # Allows the strategy ladder: curl_cffi -> playwright -> vendor unlocker.
    escalate: Optional[Callable[[Request, int], tuple[Fetcher, ProxyProvider]]] = None


@dataclass
class RunResult:
    run_id: uuid.UUID
    requests: int = 0
    ok: int = 0
    retried: int = 0
    blocked: int = 0
    dlq: int = 0
    extracted: int = 0
    extraction_failures: int = 0


class _HostRateLimiter:
    """Per-host token bucket. One request per ``min_interval_s`` per host."""

    def __init__(self, per_host_per_s: float):
        self._min_interval = 1.0 / per_host_per_s if per_host_per_s > 0 else 0.0
        self._last: dict[str, float] = {}
        self._lock = threading.Lock()

    def wait(self, host: str) -> None:
        if self._min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            last = self._last.get(host, 0.0)
            wait_for = self._min_interval - (now - last)
            if wait_for > 0:
                time.sleep(wait_for)
                now = time.monotonic()
            self._last[host] = now


def _backoff(attempt: int, base: float, cap: float) -> float:
    # Decorrelated exponential backoff with jitter.
    return min(cap, random.uniform(base, base * 2 ** attempt))


class Orchestrator:
    def __init__(self, config: ScrapeConfig):
        self._cfg = config
        self._rate = _HostRateLimiter(config.rate_limit_per_host_per_s)

    def run(self, urls: Iterable[str]) -> RunResult:
        run_id = uuid.uuid4()
        result = RunResult(run_id=run_id)
        for url in urls:
            self._process_url(url, run_id, result)
        return result

    # ------------------------------------------------------------------ #

    def _process_url(self, url: str, run_id: uuid.UUID, result: RunResult) -> None:
        host = urlsplit(url).netloc
        fetcher: Fetcher = self._cfg.fetcher
        proxy: ProxyProvider = self._cfg.proxy

        for attempt in range(1, self._cfg.max_attempts + 1):
            self._rate.wait(host)
            request = Request(url=url)

            with proxy.acquire(host) as lease:
                raw = fetcher.fetch(request, lease, attempt=attempt)
                classification = classify(raw, self._cfg.detectors)
                self._persist_raw(raw, classification, run_id)
                if lease is not None:
                    lease.report(classification=classification.severity)

            result.requests += 1

            sev = classification.severity
            if sev == "ok":
                result.ok += 1
                self._extract(raw, classification, run_id, result)
                return

            if sev == "suspicious":
                # Suspicious but not provably bad: persist + extract anyway,
                # but bump the warning counter; alerting decides what to do.
                result.ok += 1
                self._extract(raw, classification, run_id, result)
                log.warning(
                    "suspicious response url=%s flags=%s", url, classification.flags
                )
                return

            if sev == "dlq":
                result.dlq += 1
                self._cfg.storage.write_failure(
                    ExtractionFailure(
                        raw_response_id=uuid.UUID(int=0),  # raw row id linkage left to storage
                        reason=_dlq_reason(classification),
                        error_message=", ".join(classification.flags),
                    )
                )
                return

            if sev == "blocked":
                result.blocked += 1
                if self._cfg.escalate is not None:
                    fetcher, proxy = self._cfg.escalate(request, attempt)
                # fall through to retry

            if sev in {"retryable", "blocked"} and attempt < self._cfg.max_attempts:
                result.retried += 1
                time.sleep(_backoff(attempt, self._cfg.base_backoff_s, self._cfg.max_backoff_s))
                continue

            # Out of attempts; record as DLQ.
            result.dlq += 1
            self._cfg.storage.write_failure(
                ExtractionFailure(
                    raw_response_id=uuid.UUID(int=0),
                    reason="max_attempts_exhausted",
                    error_message=f"last severity={sev}, flags={classification.flags}",
                )
            )
            return

    # ------------------------------------------------------------------ #

    def _persist_raw(self, raw: RawResponse, classification: Classification, run_id: uuid.UUID) -> RawResponseRecord:
        record = RawResponseRecord.from_raw(raw, run_id=run_id, classification=classification)
        self._cfg.storage.write_raw(record)
        return record

    def _extract(
        self,
        raw: RawResponse,
        classification: Classification,
        run_id: uuid.UUID,
        result: RunResult,
    ) -> None:
        # Re-build the persisted record so the extractor and downstream
        # consumers share the same id space.
        record = RawResponseRecord.from_raw(raw, run_id=run_id, classification=classification)
        try:
            extraction = self._cfg.extractor.extract(record)
        except Exception as e:  # extractor bug -> failure row, do not blow up the run
            self._cfg.storage.write_failure(
                ExtractionFailure(
                    raw_response_id=record.id,
                    reason="parse_error",
                    error_class=type(e).__name__,
                    error_message=str(e),
                    traceback=traceback.format_exc(limit=8),
                )
            )
            result.extraction_failures += 1
            return

        if extraction.failure is not None:
            self._cfg.storage.write_failure(extraction.failure)
            result.extraction_failures += 1
        if extraction.records:
            self._cfg.storage.write_extracted(extraction.records)
            result.extracted += len(extraction.records)


def _dlq_reason(classification: Classification) -> str:
    # Pick the most informative flag for the failure row.
    for f in classification.findings:
        if f.severity in {"dlq", "blocked"}:
            return f.name
    return "unknown"
