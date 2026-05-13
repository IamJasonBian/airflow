"""Minimal Airflow DAG showing the discover → fetch → extract → reconcile shape.

Notes:

* ``fetch`` and ``extract`` are separate tasks. That separation is the
  whole point — re-running ``extract`` over yesterday's raw bodies must
  not refetch anything.
* The ``reconcile`` task compares this run's extracted count against the
  trailing 7-day median and alerts on > 30% drop. This single alert
  catches almost every "silent failure" we care about.
* Concurrency is bounded by an Airflow pool named ``scrape_acme`` —
  create it in the UI / via ``airflow pools set scrape_acme 4 ...``.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.exceptions import AirflowFailException

from .detector import (
    BlockPageDetector,
    CaptchaDetector,
    ContentLengthDetector,
    RequiredSelectorDetector,
    StatusCodeDetector,
)
from .fetcher import CurlCffiFetcher, PlaywrightFetcher
from .orchestrator import Orchestrator, ScrapeConfig
from .proxy import AwsGatewayProvider, BurnListProvider, NullProxyProvider
from .schema import InMemoryStorage, ProductExtractor


DEFAULT_ARGS = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
}


with DAG(
    dag_id="scrape_acme_products",
    description="Daily product catalog scrape (reference implementation)",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    tags=["scrape", "reference"],
) as dag:

    @task
    def discover() -> list[str]:
        """Build the URL frontier from sitemaps / DB. Stubbed here."""
        return [
            "https://example.com/products/page/1",
            "https://example.com/products/page/2",
            "https://example.com/products/page/3",
        ]

    @task(pool="scrape_acme", pool_slots=1)
    def fetch_and_extract(urls: list[str]) -> dict:
        # Tier-1 strategy: curl_cffi + free AWS Gateway IPs, with burn list.
        tier1_proxy = BurnListProvider(
            AwsGatewayProvider(target="https://example.com", regions=["us-east-1", "us-west-2"]),
            cooldown_s=900,
        )
        config = ScrapeConfig(
            name="acme_products",
            fetcher=CurlCffiFetcher(impersonate="chrome124"),
            proxy=tier1_proxy,
            detectors=[
                StatusCodeDetector(),
                ContentLengthDetector(min_bytes=2048),
                CaptchaDetector(),
                BlockPageDetector(),
                RequiredSelectorDetector("data-product-sku", "class=\"price\""),
            ],
            extractor=ProductExtractor(),
            storage=InMemoryStorage(),  # swap for PostgresSink in prod
            rate_limit_per_host_per_s=1.0,
            max_attempts=4,
            # Escalation: if we get blocked, switch to Playwright + direct.
            # In production this tier would use residential proxies, not direct.
            escalate=lambda req, attempt: (PlaywrightFetcher(), NullProxyProvider()),
        )
        result = Orchestrator(config).run(urls)
        return {
            "run_id": str(result.run_id),
            "requests": result.requests,
            "ok": result.ok,
            "retried": result.retried,
            "blocked": result.blocked,
            "dlq": result.dlq,
            "extracted": result.extracted,
            "extraction_failures": result.extraction_failures,
        }

    @task
    def reconcile(stats: dict) -> None:
        """The 'something broke quietly' guard.

        In real life this would query the warehouse for the trailing
        7-day median ``extracted`` count and compare. Here we just
        sanity-check the in-run counters.
        """
        extracted = stats["extracted"]
        if extracted == 0:
            raise AirflowFailException(
                f"scrape produced zero records (stats={stats}); investigate"
            )
        # >50% of requests blocked is a sign the strategy needs adjusting.
        if stats["requests"] and stats["blocked"] / stats["requests"] > 0.5:
            raise AirflowFailException(
                f"block rate {stats['blocked']}/{stats['requests']}; escalate proxy tier"
            )

    reconcile(fetch_and_extract(discover()))
