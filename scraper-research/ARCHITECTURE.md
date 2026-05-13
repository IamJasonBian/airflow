# Scraper architecture

How to make a scraper *flexible*, *observable*, and *robust against silent
failure*. This document covers schema, the pluggable interfaces, the
silent-failure detection layer, and the run lifecycle.

## Goals

1. **Swappable everywhere.** Fetcher, proxy provider, extractor, sink,
   rate limiter, and detectors are all behind narrow protocols. You
   should be able to migrate from `httpx` to `curl_cffi` to Playwright
   without touching the orchestrator.
2. **Raw is sacred.** Persist the raw response *before* extraction.
   Extraction logic changes; the bytes you fetched do not. Re-running
   extraction must be free.
3. **Fail loudly, then fail safely.** A 200 OK that returns a Cloudflare
   challenge page is the worst kind of bug. Validate every response,
   classify failures, and route them to retry / DLQ / alert.
4. **No half-records.** A row in `extracted_*` exists only if it passed
   schema validation. Everything else lives in `raw_response` and
   `extraction_failure`.

## The pluggable interfaces

```
                ┌────────────────────────────────────────────┐
                │              Orchestrator                  │
                │  (rate limit, retries, per-domain config)  │
                └───────┬──────────────┬──────────────┬──────┘
                        │              │              │
                        ▼              ▼              ▼
                ┌──────────────┐ ┌────────────┐ ┌────────────┐
                │   Fetcher    │ │  Proxy     │ │ Detector   │
                │  (Protocol)  │ │ (Protocol) │ │ (Protocol) │
                └──────┬───────┘ └──────┬─────┘ └──────┬─────┘
                       │                │              │
       ┌───────────────┼─────────┐      │     ┌────────┼──────────┐
       ▼               ▼         ▼      ▼     ▼        ▼          ▼
  httpx-fetch   curl_cffi   playwright AWS-GW Bright captcha- soft-404-
                                              Data   detect    detect
                       │
                       ▼
                ┌──────────────┐         ┌──────────────┐
                │   Extractor  │────────▶│  Storage     │
                │  (Protocol)  │         │  (Protocol)  │
                └──────────────┘         └──────────────┘
```

Each protocol is intentionally narrow:

- `Fetcher.fetch(request) -> RawResponse`
- `ProxyProvider.acquire(domain) -> ProxyLease` (context-managed)
- `Detector.check(raw) -> DetectionResult`
- `Extractor.extract(raw) -> ExtractionResult`
- `Storage.write_raw(raw)` / `write_extracted(rec)` / `write_failure(f)`

This is "ports and adapters" — Hexagonal architecture. The orchestrator
depends only on protocols; concrete implementations are injected per
DAG / job.

## Schema design

Three core tables, plus one job-tracking table. Designed for Postgres
but maps cleanly onto BigQuery / Snowflake (use `JSON` / `VARIANT` for
the payload columns).

### `scrape_run`

Tracks a single execution of a scrape job (one Airflow task run).

| col              | type        | notes                                      |
| ---------------- | ----------- | ------------------------------------------ |
| id               | uuid pk     |                                            |
| job_name         | text        | matches DAG/task name                      |
| started_at       | timestamptz |                                            |
| finished_at      | timestamptz | nullable                                   |
| status           | text        | running / success / partial / failed       |
| config_hash      | text        | sha256 of effective config (versioning)    |
| counters         | jsonb       | {requests, ok, retries, dlq, captcha, ...} |
| airflow_run_id   | text        | nullable; for cross-linking                |

### `raw_response`

The source of truth. Every fetch attempt ends up here, success or fail.

| col              | type        | notes                                      |
| ---------------- | ----------- | ------------------------------------------ |
| id               | uuid pk     |                                            |
| run_id           | uuid fk     | → scrape_run                               |
| url              | text        | canonicalized (via `w3lib.url`)            |
| url_hash         | bytea       | sha256(url) — index for dedupe             |
| method           | text        | GET / POST                                 |
| request_headers  | jsonb       | redacted (no auth tokens stored)           |
| request_body_hash| bytea       | nullable                                   |
| status_code      | int         | nullable on network failure                |
| response_headers | jsonb       |                                            |
| body             | bytea       | gzipped HTML/JSON; can offload to S3       |
| body_hash        | bytea       | sha256(body) — dedupe + change detection   |
| body_bytes       | int         | uncompressed size                          |
| content_type     | text        |                                            |
| fetched_at       | timestamptz |                                            |
| fetcher          | text        | "curl_cffi" / "playwright" / "httpx"       |
| proxy_id         | text        | opaque id of proxy lease                   |
| attempt          | int         | retry attempt number, 1-indexed            |
| duration_ms      | int         |                                            |
| detection_flags  | text[]      | results of detectors (see below)           |
| classification   | text        | ok / retryable / blocked / dlq             |

**Why keep the raw body forever?** Extraction is the part you'll
iterate on. Selector drift, new fields, schema migrations — all of
them should be re-runnable without re-fetching. If body storage cost
becomes real, tier it: hot in Postgres for N days, cold in S3.

### `extraction` (per record type)

One table *per logical record type* (e.g. `extracted_product`,
`extracted_review`). Generic shape:

| col              | type        | notes                                      |
| ---------------- | ----------- | ------------------------------------------ |
| id               | uuid pk     |                                            |
| raw_response_id  | uuid fk     | → raw_response                             |
| natural_key      | text        | e.g. SKU, listing id; indexed              |
| schema_version   | int         | bump on breaking changes                   |
| payload          | jsonb       | pydantic-validated record                  |
| extracted_at     | timestamptz |                                            |

Why a typed table per record type instead of one big EAV? Querying. You
want `select avg(price) from extracted_product where ...` to be a fast,
indexed scan, not a `jsonb_path` filter.

Why also a `payload` jsonb column on top of typed columns? Pragmatism.
Typed columns for the dozen fields you actually filter on; jsonb for the
long tail of "we'll need this someday" fields. Keep both in sync via
Pydantic.

### `extraction_failure`

The DLQ. Every failed extraction is a row here, *not* discarded.

| col              | type        | notes                                      |
| ---------------- | ----------- | ------------------------------------------ |
| id               | uuid pk     |                                            |
| raw_response_id  | uuid fk     |                                            |
| reason           | text        | enum: missing_field / parse_error / blocked / captcha / soft_404 / schema_mismatch |
| error_class      | text        |                                            |
| error_message    | text        |                                            |
| traceback        | text        | trimmed                                    |
| failed_at        | timestamptz |                                            |
| resolved_at      | timestamptz | set when reprocessed successfully          |

A nightly DAG re-runs extraction over `extraction_failure` rows whose
`raw_response.body_hash` still matches — if your extractor improved,
they resolve automatically.

## Silent-failure detection

The thing that bites every scraper: HTTP 200 + HTML body + zero useful
data. The `Detector` protocol runs a chain of cheap checks on every
response *before* classification:

| Detector                  | Signal                                                                |
| ------------------------- | --------------------------------------------------------------------- |
| `StatusCodeDetector`      | non-2xx → `retryable` (5xx, 429, 408) or `blocked` (403, 451)         |
| `ContentLengthDetector`   | body unreasonably small for the URL pattern → `suspicious`            |
| `CaptchaDetector`         | known fingerprints: "challenge-platform", "g-recaptcha", hCaptcha     |
| `BlockPageDetector`       | known WAF strings: "Access Denied", "Pardon Our Interruption", etc.   |
| `Soft404Detector`         | 200 but body matches per-domain "not found" template hash             |
| `RequiredSelectorDetector`| per-target: required CSS selector(s) missing → likely block / change  |
| `ContentHashDetector`     | body_hash matches known-bad page hash (cached per domain)             |
| `SchemaDetector`          | extracted payload fails Pydantic validation                           |

Each detector returns `(name, severity, evidence)`. Severities map to
`classification` on the raw response:

- `ok` → write extraction
- `suspicious` → write extraction *and* a warning row; alert if rate > threshold
- `retryable` → retry with new proxy + UA, capped by attempt count
- `blocked` → cooldown this proxy, retry with a different provider tier
- `dlq` → write to `extraction_failure`, do not retry; alert

**Per-domain "known bad" hash table.** When an operator confirms a
block page, we hash it and store it. Future fetches matching that hash
short-circuit straight to `blocked`. Cheap, effective.

## Failure-handling rules of thumb

1. **Retries have a budget per URL** (`max_attempts`, default 4) *and*
   per run (`max_total_retries`). A poison URL can't burn the whole run.
2. **Exponential backoff with jitter.** `tenacity.wait_random_exponential`.
3. **Change one variable per retry.** New proxy *or* new UA *or*
   different fetcher — not all three. Helps diagnose which axis was
   blocking.
4. **Per-domain circuit breaker.** N consecutive failures within a window
   → trip the breaker, alert, mark remaining URLs `deferred` for the
   next run. Cheaper than slamming a hostile origin.
5. **Adaptive concurrency.** Start at 1 req/s/domain. Increase on
   sustained success. Halve on first 429 / block.
6. **Polite defaults.** Honour `robots.txt`, send a real User-Agent that
   identifies the bot for first-party owned scrapes, set a contact email
   header where appropriate. Override per-domain only when intentional.
7. **Idempotency.** `url_hash` + `body_hash` lets you safely re-fetch.
   `natural_key` + `schema_version` lets you upsert extractions.

## Configuration: how flexibility shows up in practice

A scrape is fully described by a config object that the orchestrator
consumes. Per-domain overrides are merged on top of defaults.

```python
ScrapeConfig(
    name="acme_products",
    seed_urls=[...],
    fetcher="curl_cffi",                # or "playwright" / "httpx"
    proxy="aws_gateway",                # or "brightdata_residential"
    rate_limit_per_host="1/s",
    max_attempts=4,
    concurrency=8,
    detectors=[
        "status",
        "captcha",
        "block_page",
        RequiredSelector("div.product-title"),
        Soft404("acme.example.com", body_template_hash="..."),
    ],
    extractor=ProductExtractor(schema_version=3),
    storage=PostgresSink(dsn=...),
    on_block="escalate",                # next-tier proxy
    obey_robots=True,
)
```

Anything site-specific lives in a `sites/<domain>.yaml` file checked
into the repo. Code stays generic; behaviour is data.

## Observability

- **Structured logs** (`structlog`): every event carries `run_id`,
  `url_hash`, `fetcher`, `proxy_id`, `attempt`, `classification`.
- **Metrics** (StatsD/Prometheus): `scrape.requests`,
  `scrape.requests.classification`, `scrape.duration_ms`,
  `scrape.proxy.errors`, `scrape.extraction.failures`.
- **Run summary**: every scrape_run gets a row in `scrape_run` with
  counters; an Airflow on-success callback compares against last run
  and alerts on > X% drop in extracted count (the single best
  "something broke quietly" signal).

The "extracted-count delta" alert is the one alert you must have.

## Airflow shape

- One DAG per logical scrape job. Each DAG = `discover → fetch →
  extract → load → reconcile`.
- `discover` builds the URL frontier from seed pages / sitemaps / DB.
- `fetch` runs the orchestrator in a `KubernetesPodOperator` or
  `DockerOperator` so each scrape has its own egress IP and resource
  isolation.
- `extract` is *separate* — it reads from `raw_response` and writes
  `extraction` / `extraction_failure`. This split is what makes
  "rerun extraction without refetching" possible.
- `reconcile` checks counters, alerts on drift, retries DLQ rows whose
  body_hash matches an updated extractor schema_version.

See `reference/example_dag.py` for a minimal end-to-end skeleton.

## What's intentionally not in v1

- Distributed crawling (Scrapy-Redis style). Airflow + a URL frontier
  table is enough until we're sustainably > 100 req/s.
- Auto-CAPTCHA solving. Detect → escalate to vendor unlocker tier;
  don't try to solve in-process.
- ML-based extractor (the "generic article extractor" pattern). Worth
  doing later for unknown sites; deterministic extractors per
  high-value target first.
