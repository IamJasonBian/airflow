"""Proxy / IP rotation strategies.

Every implementation produces ``ProxyLease`` objects via a context manager.
A lease is the smallest unit of "an IP I currently hold"; the orchestrator
calls ``report()`` on it after each request so the provider can update its
internal scoring (burn list, sticky session lifetime, etc.).

Implementations:

* ``NullProxyProvider``       — no proxy (direct).
* ``StaticPoolProvider``      — round-robins a list of URLs.
* ``AwsGatewayProvider``      — `requests-ip-rotator`: free, AWS API Gateway IPs.
* ``CommercialProxyProvider`` — template for Bright Data / Oxylabs / SOAX.
* ``BurnListProvider``        — wraps another provider, evicts on bad signals.
"""

from __future__ import annotations

import itertools
import random
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Iterator, List, Optional, Protocol


@dataclass
class ProxyLease:
    id: str
    url: str  # e.g. "http://user:pass@host:port"
    username: Optional[str] = None
    password: Optional[str] = None
    sticky_until: Optional[float] = None  # epoch seconds
    metadata: dict = field(default_factory=dict)

    def report(self, *, classification: str) -> None:
        """Called by the orchestrator after each request using this lease.

        Concrete providers may override behaviour via the closure that
        produced the lease — see ``BurnListProvider``.
        """
        # default no-op; providers attach a callback via metadata if needed
        cb = self.metadata.get("on_report")
        if cb:
            cb(self, classification)


class ProxyProvider(Protocol):
    name: str

    @contextmanager
    def acquire(self, domain: str) -> Iterator[Optional[ProxyLease]]: ...


# --------------------------------------------------------------------------- #

class NullProxyProvider:
    """No proxy. Direct egress."""

    name = "none"

    @contextmanager
    def acquire(self, domain: str) -> Iterator[Optional[ProxyLease]]:
        yield None


# --------------------------------------------------------------------------- #

class StaticPoolProvider:
    """Round-robin over a fixed list of proxy URLs.

    Use for: a cheap pre-purchased datacenter proxy list.
    """

    def __init__(self, urls: List[str], *, name: str = "static_pool"):
        if not urls:
            raise ValueError("StaticPoolProvider needs at least one url")
        self.name = name
        self._urls = list(urls)
        self._cycle = itertools.cycle(self._urls)
        self._lock = threading.Lock()

    @contextmanager
    def acquire(self, domain: str) -> Iterator[Optional[ProxyLease]]:
        with self._lock:
            url = next(self._cycle)
        yield ProxyLease(id=f"static:{hash(url) & 0xffff:04x}", url=url)


# --------------------------------------------------------------------------- #

class AwsGatewayProvider:
    """Free IP rotation via AWS API Gateway (`requests-ip-rotator`).

    Each request is tunneled through a regional API Gateway endpoint; AWS
    rotates the egress IP from the public AWS NAT pool. Practically free
    under the API Gateway free tier.

    Limitations:
      * HTTPS to the *target* only (gateway terminates TLS to AWS).
      * AWS IP ranges are sometimes blocked outright.
      * Geo: you pick a region, but exit IPs are AWS-owned, not residential.

    Usage:
        provider = AwsGatewayProvider(target="https://api.example.com",
                                      regions=["us-east-1", "eu-west-1"])
        with provider.acquire("api.example.com") as lease:
            ...
        provider.close()  # tears down the gateways
    """

    name = "aws_gateway"

    def __init__(self, target: str, regions: Optional[List[str]] = None):
        self._target = target
        self._regions = regions or ["us-east-1"]
        self._gateway = None  # lazy

    def _ensure_started(self):
        if self._gateway is not None:
            return
        from requests_ip_rotator import ApiGateway  # lazy

        self._gateway = ApiGateway(self._target, regions=self._regions)
        self._gateway.start()

    @contextmanager
    def acquire(self, domain: str) -> Iterator[Optional[ProxyLease]]:
        self._ensure_started()
        # requests-ip-rotator works by mounting an adapter onto a session,
        # not by handing back a proxy URL. We surface that detail via
        # metadata; the fetcher honours it.
        lease = ProxyLease(
            id=f"awsgw:{random.randint(0, 1 << 24):06x}",
            url="",  # not a real proxy URL
            metadata={"requests_ip_rotator_session": self._gateway},
        )
        yield lease

    def close(self):
        if self._gateway is not None:
            self._gateway.shutdown()
            self._gateway = None


# --------------------------------------------------------------------------- #

class CommercialProxyProvider:
    """Generic template for residential / mobile proxy vendors.

    Bright Data, Oxylabs, Smartproxy, SOAX, IPRoyal all converge on the
    same shape: a host:port with username-encoded session/geo/sticky flags
    in the auth.

    Example (Bright Data sticky session, US, 10-minute lifetime):
        host = "brd.superproxy.io:22225"
        username = "brd-customer-XXX-zone-residential-country-us-session-{session}"
        password = "..."
        sticky_for = 600

    The provider mints a per-domain (or per-call) session id, formats the
    username, and returns a ProxyLease.
    """

    def __init__(
        self,
        *,
        name: str,
        host: str,
        username_template: str,
        password: str,
        sticky_for_s: int = 0,
    ):
        self.name = name
        self._host = host
        self._username_template = username_template
        self._password = password
        self._sticky_for_s = sticky_for_s
        self._sessions: dict[str, tuple[str, float]] = {}  # domain -> (session_id, expiry)
        self._lock = threading.Lock()

    def _session_for(self, domain: str) -> str:
        if self._sticky_for_s <= 0:
            return f"{random.randint(0, 1 << 28):08x}"
        with self._lock:
            sid, expiry = self._sessions.get(domain, ("", 0.0))
            if sid and time.time() < expiry:
                return sid
            sid = f"{random.randint(0, 1 << 28):08x}"
            self._sessions[domain] = (sid, time.time() + self._sticky_for_s)
            return sid

    @contextmanager
    def acquire(self, domain: str) -> Iterator[Optional[ProxyLease]]:
        session = self._session_for(domain)
        username = self._username_template.format(session=session, domain=domain)
        url = f"http://{username}:{self._password}@{self._host}"
        yield ProxyLease(
            id=f"{self.name}:{session}",
            url=url,
            username=username,
            password=self._password,
            sticky_until=time.time() + self._sticky_for_s if self._sticky_for_s else None,
        )


# --------------------------------------------------------------------------- #

class BurnListProvider:
    """Wrap another provider; evict leases that report `blocked` / `captcha`.

    Burns are per (domain, lease-key); cooldown is configurable. The wrapped
    provider is asked for another lease if a burned one comes back, up to
    ``max_tries`` attempts per acquire.
    """

    def __init__(self, inner: ProxyProvider, *, cooldown_s: int = 600, max_tries: int = 3):
        self.name = f"burnlist({inner.name})"
        self._inner = inner
        self._cooldown_s = cooldown_s
        self._max_tries = max_tries
        self._burns: dict[tuple[str, str], float] = {}  # (domain, lease_id) -> expiry
        self._lock = threading.Lock()

    def _is_burned(self, domain: str, lease_id: str) -> bool:
        with self._lock:
            expiry = self._burns.get((domain, lease_id))
            if not expiry:
                return False
            if time.time() >= expiry:
                self._burns.pop((domain, lease_id), None)
                return False
            return True

    def _burn(self, domain: str, lease_id: str) -> None:
        with self._lock:
            self._burns[(domain, lease_id)] = time.time() + self._cooldown_s

    @contextmanager
    def acquire(self, domain: str) -> Iterator[Optional[ProxyLease]]:
        for _ in range(self._max_tries):
            with self._inner.acquire(domain) as lease:
                if lease is None:
                    yield None
                    return
                if self._is_burned(domain, lease.id):
                    continue

                def _on_report(le: ProxyLease, classification: str, _self=self, _dom=domain):
                    if classification in {"blocked", "captcha"}:
                        _self._burn(_dom, le.id)

                lease.metadata["on_report"] = _on_report
                yield lease
                return
        # All attempts burned; surface None so the orchestrator escalates tier.
        yield None
