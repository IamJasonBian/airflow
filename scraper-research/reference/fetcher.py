"""Fetcher protocol + concrete implementations.

Three implementations are provided as a strategy ladder:

  httpx_fetcher    — polite, no anti-bot. For friendly APIs / sitemaps.
  curl_cffi_fetcher — TLS fingerprint impersonation; default for hostile sites.
  playwright_fetcher — full browser, for JS-rendered / Turnstile-style targets.

The orchestrator only ever sees the `Fetcher` Protocol. Add a new backend
by implementing one method.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Mapping, Optional, Protocol

from .proxy import ProxyLease


@dataclass(frozen=True)
class Request:
    url: str
    method: str = "GET"
    headers: Mapping[str, str] = field(default_factory=dict)
    body: Optional[bytes] = None
    timeout_s: float = 30.0
    # If True, the fetcher should render JS (browser backends only).
    render_js: bool = False


@dataclass
class RawResponse:
    request: Request
    status_code: Optional[int]
    headers: Mapping[str, str]
    body: bytes
    fetched_at: float
    duration_ms: int
    fetcher: str
    proxy_id: Optional[str]
    attempt: int
    error: Optional[str] = None  # set when the fetch itself raised

    @property
    def ok(self) -> bool:
        return self.error is None and self.status_code is not None and 200 <= self.status_code < 300


class Fetcher(Protocol):
    name: str

    def fetch(self, request: Request, proxy: Optional[ProxyLease], attempt: int) -> RawResponse: ...


# --------------------------------------------------------------------------- #
# httpx — polite default                                                      #
# --------------------------------------------------------------------------- #

class HttpxFetcher:
    """Plain httpx. No anti-bot tricks. Use for first-party APIs / sitemaps."""

    name = "httpx"

    def __init__(self, default_headers: Optional[Mapping[str, str]] = None):
        self._default_headers = dict(default_headers or {})

    def fetch(self, request: Request, proxy: Optional[ProxyLease], attempt: int) -> RawResponse:
        import httpx  # lazy

        start = time.monotonic()
        fetched_at = time.time()
        proxies = {"all://": proxy.url} if proxy else None
        try:
            with httpx.Client(proxies=proxies, timeout=request.timeout_s, follow_redirects=True) as c:
                resp = c.request(
                    request.method,
                    request.url,
                    headers={**self._default_headers, **dict(request.headers)},
                    content=request.body,
                )
            return RawResponse(
                request=request,
                status_code=resp.status_code,
                headers=dict(resp.headers),
                body=resp.content,
                fetched_at=fetched_at,
                duration_ms=int((time.monotonic() - start) * 1000),
                fetcher=self.name,
                proxy_id=proxy.id if proxy else None,
                attempt=attempt,
            )
        except Exception as e:
            return RawResponse(
                request=request,
                status_code=None,
                headers={},
                body=b"",
                fetched_at=fetched_at,
                duration_ms=int((time.monotonic() - start) * 1000),
                fetcher=self.name,
                proxy_id=proxy.id if proxy else None,
                attempt=attempt,
                error=f"{type(e).__name__}: {e}",
            )


# --------------------------------------------------------------------------- #
# curl_cffi — TLS fingerprint impersonation. The default for hostile sites.   #
# --------------------------------------------------------------------------- #

class CurlCffiFetcher:
    """curl_cffi with browser TLS impersonation.

    Defeats JA3/JA4 fingerprint blocking which plain httpx/requests trip on
    Cloudflare-protected origins. Same API surface as `requests`.
    """

    name = "curl_cffi"

    def __init__(self, impersonate: str = "chrome124", default_headers: Optional[Mapping[str, str]] = None):
        # `impersonate` rotates over time as Chrome ships; keep configurable.
        self._impersonate = impersonate
        self._default_headers = dict(default_headers or {})

    def fetch(self, request: Request, proxy: Optional[ProxyLease], attempt: int) -> RawResponse:
        from curl_cffi import requests as cc_requests  # lazy

        start = time.monotonic()
        fetched_at = time.time()
        proxies = {"http": proxy.url, "https": proxy.url} if proxy else None
        try:
            resp = cc_requests.request(
                request.method,
                request.url,
                headers={**self._default_headers, **dict(request.headers)},
                data=request.body,
                proxies=proxies,
                timeout=request.timeout_s,
                impersonate=self._impersonate,
                allow_redirects=True,
            )
            return RawResponse(
                request=request,
                status_code=resp.status_code,
                headers=dict(resp.headers),
                body=resp.content,
                fetched_at=fetched_at,
                duration_ms=int((time.monotonic() - start) * 1000),
                fetcher=self.name,
                proxy_id=proxy.id if proxy else None,
                attempt=attempt,
            )
        except Exception as e:
            return RawResponse(
                request=request,
                status_code=None,
                headers={},
                body=b"",
                fetched_at=fetched_at,
                duration_ms=int((time.monotonic() - start) * 1000),
                fetcher=self.name,
                proxy_id=proxy.id if proxy else None,
                attempt=attempt,
                error=f"{type(e).__name__}: {e}",
            )


# --------------------------------------------------------------------------- #
# Playwright — heavyweight, for JS rendering / Turnstile-class defences       #
# --------------------------------------------------------------------------- #

class PlaywrightFetcher:
    """Playwright + playwright-stealth. Slow, expensive, defeats most defences.

    Reuses a single browser per fetcher instance; pages are short-lived. The
    `route()` call below drops images/fonts/media which typically halves
    fetch time on heavy pages.
    """

    name = "playwright"

    _BLOCK_RESOURCE_TYPES = {"image", "media", "font", "stylesheet"}

    def __init__(self, headless: bool = True, block_resources: bool = True):
        self._headless = headless
        self._block_resources = block_resources
        self._pw = None  # lazy
        self._browser = None

    def _ensure_started(self):
        if self._browser is not None:
            return
        from playwright.sync_api import sync_playwright  # lazy

        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=self._headless)

    def fetch(self, request: Request, proxy: Optional[ProxyLease], attempt: int) -> RawResponse:
        from playwright_stealth import stealth_sync  # lazy

        self._ensure_started()
        start = time.monotonic()
        fetched_at = time.time()
        ctx_kwargs = {}
        if proxy:
            ctx_kwargs["proxy"] = {"server": proxy.url, "username": proxy.username, "password": proxy.password}
        context = self._browser.new_context(**ctx_kwargs)
        page = context.new_page()
        stealth_sync(page)

        if self._block_resources:
            page.route(
                "**/*",
                lambda route: route.abort()
                if route.request.resource_type in self._BLOCK_RESOURCE_TYPES
                else route.continue_(),
            )

        try:
            resp = page.goto(request.url, timeout=request.timeout_s * 1000, wait_until="domcontentloaded")
            body = page.content().encode("utf-8")
            status = resp.status if resp else None
            headers = dict(resp.headers) if resp else {}
            return RawResponse(
                request=request,
                status_code=status,
                headers=headers,
                body=body,
                fetched_at=fetched_at,
                duration_ms=int((time.monotonic() - start) * 1000),
                fetcher=self.name,
                proxy_id=proxy.id if proxy else None,
                attempt=attempt,
            )
        except Exception as e:
            return RawResponse(
                request=request,
                status_code=None,
                headers={},
                body=b"",
                fetched_at=fetched_at,
                duration_ms=int((time.monotonic() - start) * 1000),
                fetcher=self.name,
                proxy_id=proxy.id if proxy else None,
                attempt=attempt,
                error=f"{type(e).__name__}: {e}",
            )
        finally:
            context.close()

    def close(self):
        if self._browser is not None:
            self._browser.close()
        if self._pw is not None:
            self._pw.stop()
