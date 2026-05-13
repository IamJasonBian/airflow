"""Silent-failure detectors.

A scrape that returns HTTP 200 with a Cloudflare challenge body is the
worst class of bug — it pollutes downstream tables with empty records
and never alerts. The detector chain runs on every response *before*
extraction and produces a classification used by the orchestrator to
decide retry / escalate / DLQ.

Add detectors freely; they are cheap. Order does not matter — the
orchestrator aggregates by max severity.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Protocol, Sequence

from .fetcher import RawResponse


# Severity ladder. Higher = worse.
SEVERITY = {
    "ok": 0,
    "suspicious": 1,
    "retryable": 2,
    "blocked": 3,
    "dlq": 4,
}


@dataclass
class DetectionResult:
    name: str
    severity: str  # one of SEVERITY keys
    evidence: str = ""

    @property
    def rank(self) -> int:
        return SEVERITY[self.severity]


@dataclass
class Classification:
    severity: str
    findings: List[DetectionResult] = field(default_factory=list)

    @property
    def flags(self) -> List[str]:
        return [f"{f.name}:{f.severity}" for f in self.findings]


class Detector(Protocol):
    name: str

    def check(self, raw: RawResponse) -> Optional[DetectionResult]: ...


def classify(raw: RawResponse, detectors: Sequence[Detector]) -> Classification:
    findings: List[DetectionResult] = []
    for d in detectors:
        try:
            r = d.check(raw)
        except Exception as e:  # detectors must never crash the pipeline
            r = DetectionResult(d.name, "suspicious", f"detector error: {e!r}")
        if r is not None:
            findings.append(r)
    severity = "ok"
    for f in findings:
        if f.rank > SEVERITY[severity]:
            severity = f.severity
    return Classification(severity=severity, findings=findings)


# --------------------------------------------------------------------------- #
# Built-in detectors                                                          #
# --------------------------------------------------------------------------- #

class StatusCodeDetector:
    """Map HTTP status → severity."""

    name = "status"

    def check(self, raw: RawResponse) -> Optional[DetectionResult]:
        if raw.error is not None:
            return DetectionResult(self.name, "retryable", raw.error)
        sc = raw.status_code
        if sc is None:
            return DetectionResult(self.name, "retryable", "no status code")
        if 200 <= sc < 300:
            return None
        if sc in (408, 425, 429, 500, 502, 503, 504):
            return DetectionResult(self.name, "retryable", f"status {sc}")
        if sc in (401, 403, 451):
            return DetectionResult(self.name, "blocked", f"status {sc}")
        if sc == 404:
            return DetectionResult(self.name, "dlq", "status 404")
        return DetectionResult(self.name, "suspicious", f"status {sc}")


class ContentLengthDetector:
    """Body unreasonably small for what we expected."""

    name = "content_length"

    def __init__(self, min_bytes: int = 512):
        self._min_bytes = min_bytes

    def check(self, raw: RawResponse) -> Optional[DetectionResult]:
        if raw.error is not None or not raw.ok:
            return None
        if len(raw.body) < self._min_bytes:
            return DetectionResult(self.name, "suspicious", f"body {len(raw.body)}B < {self._min_bytes}B")
        return None


class CaptchaDetector:
    """Known captcha/challenge fingerprints in the response body."""

    name = "captcha"

    _PATTERNS = [
        re.compile(rb"challenge-platform", re.I),
        re.compile(rb"cf-chl-bypass", re.I),
        re.compile(rb"g-recaptcha", re.I),
        re.compile(rb"hcaptcha\.com", re.I),
        re.compile(rb"data-sitekey", re.I),
        re.compile(rb"turnstile/v0/api", re.I),
    ]

    def check(self, raw: RawResponse) -> Optional[DetectionResult]:
        if not raw.body:
            return None
        for p in self._PATTERNS:
            m = p.search(raw.body)
            if m:
                return DetectionResult(self.name, "blocked", f"matched {m.group(0)!r}")
        return None


class BlockPageDetector:
    """Known WAF / block page strings."""

    name = "block_page"

    _PATTERNS = [
        re.compile(rb"Access Denied", re.I),
        re.compile(rb"Pardon Our Interruption", re.I),  # PerimeterX
        re.compile(rb"Request unsuccessful\. Incapsula", re.I),
        re.compile(rb"Reference\s*#\s*\d+\.[0-9a-f]+", re.I),  # Akamai
        re.compile(rb"<title>\s*Just a moment", re.I),  # CF 5s IUAM
        re.compile(rb"blocked because we believe you are using automation", re.I),
    ]

    def check(self, raw: RawResponse) -> Optional[DetectionResult]:
        if not raw.body:
            return None
        for p in self._PATTERNS:
            m = p.search(raw.body)
            if m:
                return DetectionResult(self.name, "blocked", f"matched {m.group(0)!r}")
        return None


class Soft404Detector:
    """Detect '200 OK but page says not found'.

    Calibrate by fetching a guaranteed-bad URL on the target domain once
    and recording its body hash. Future bodies matching that hash are
    soft 404s.
    """

    name = "soft_404"

    def __init__(self, known_bad_hashes: Iterable[str]):
        self._hashes = set(known_bad_hashes)

    def check(self, raw: RawResponse) -> Optional[DetectionResult]:
        if not raw.body:
            return None
        h = hashlib.sha256(raw.body).hexdigest()
        if h in self._hashes:
            return DetectionResult(self.name, "dlq", f"body hash {h[:12]} matches known soft-404")
        return None


class RequiredSelectorDetector:
    """Required CSS selector(s) must be present in the HTML.

    Catches the most common "extraction silently produces empty rows"
    case: the page changed and our selector no longer matches.

    The check is intentionally substring-based against the raw HTML
    rather than a full parse — it's a cheap detector, not the extractor.
    Use simple, distinctive tokens (e.g. ``data-pid=`` rather than
    ``div``).
    """

    name = "required_selector"

    def __init__(self, *tokens: str):
        if not tokens:
            raise ValueError("at least one token is required")
        self._tokens = [t.encode("utf-8") for t in tokens]
        self._human = ", ".join(tokens)

    def check(self, raw: RawResponse) -> Optional[DetectionResult]:
        if not raw.body or not raw.ok:
            return None
        missing = [t for t in self._tokens if t not in raw.body]
        if missing:
            return DetectionResult(self.name, "suspicious", f"missing tokens: {self._human}")
        return None


class KnownBadHashDetector:
    """Per-domain learned cache of confirmed-bad body hashes."""

    name = "known_bad_hash"

    def __init__(self, hashes: Iterable[str]):
        self._hashes = set(hashes)

    def add(self, body: bytes) -> None:
        self._hashes.add(hashlib.sha256(body).hexdigest())

    def check(self, raw: RawResponse) -> Optional[DetectionResult]:
        if not raw.body:
            return None
        h = hashlib.sha256(raw.body).hexdigest()
        if h in self._hashes:
            return DetectionResult(self.name, "blocked", f"body hash {h[:12]} on blocklist")
        return None
