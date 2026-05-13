# Anti-bot scraper research

Notes from comparing anti-bot HTTP/browser libraries and IP-rotation
strategies, plus a reference design (see `ARCHITECTURE.md` and
`reference/`) for a flexible, fault-tolerant scraper that can run as
Airflow DAGs.

The TL;DR up front:

| Layer            | Recommended default                             | When to upgrade                                    |
| ---------------- | ----------------------------------------------- | -------------------------------------------------- |
| HTTP fetch       | `curl_cffi` (Chrome TLS impersonation)          | Cloudflare/Akamai → `nodriver` or `playwright`     |
| Browser fetch    | `playwright` + `playwright-stealth`             | Hard targets → `nodriver` (successor of UC)        |
| IP rotation      | `requests-ip-rotator` (AWS API Gateway, free)   | Residential needed → Bright Data / Oxylabs / SOAX  |
| Parsing          | `selectolax` (fast) or `parsel` (Scrapy-style)  | JS-rendered data → JSON endpoint sniffing first    |
| Validation       | `pydantic` v2                                   | Schema-on-read → keep raw HTML always              |
| Orchestration    | Airflow `TaskFlow` + per-domain pools           | High volume → Airflow + Celery/K8s executor        |

## Anti-bot fetch libraries

Ranked roughly by "best for a new scraper, in 2026" — but the right pick
is target-specific, so the reference design treats the fetcher as a
swappable strategy.

### HTTP-level (fast, cheap)

- **`curl_cffi`** — Python binding over curl-impersonate. Mimics the TLS
  and HTTP/2 fingerprint of real Chrome/Safari/Firefox. **Solves the JA3
  fingerprint problem that breaks plain `requests`/`httpx`** on
  Cloudflare-protected sites. Sync + async. Same API surface as
  `requests`. *This is the default fetcher in the reference impl.*
- **`hrequests`** — Pure-Python stealth HTTP with TLS spoofing + optional
  embedded Chromium. Less mature than `curl_cffi` but more "batteries
  included".
- **`cloudscraper`** — Solves the old Cloudflare IUAM JS challenge.
  Largely obsolete vs Cloudflare Turnstile, but still useful for a
  surprising number of small sites.
- **`httpx` + manual headers** — No anti-bot magic, but the cleanest
  async client. Fine for friendly APIs / sitemaps / robots.txt /
  feeds. Keep this around as a "polite" fetcher.

### Browser-level (slow, expensive, defeats most defences)

- **`playwright`** + **`playwright-stealth`** — Best default browser
  stack. Cross-browser, good async story, first-party `route()`
  interception for blocking ads/trackers/images (huge speed win).
- **`nodriver`** — From the author of `undetected-chromedriver`; uses
  CDP directly with no Selenium layer. Faster and less detectable than
  UC. Use when Playwright stealth isn't enough.
- **`undetected-chromedriver`** — Still works for many targets but is
  effectively in maintenance; prefer `nodriver` for new work.
- **`botasaurus`** — All-in-one framework (browser + HTTP + anti-bot +
  storage). Productive for one-offs, opinionated, harder to embed in
  Airflow.
- **`selenium-stealth`** — Old guard. Skip unless you must use Selenium.

### Hosted "scraping APIs" (vendor solves anti-bot for you)

- **ScrapingBee**, **ZenRows**, **ScraperAPI**, **Bright Data Web
  Unlocker**, **Oxylabs Web Unlocker**.
- Treat as a fallback tier: try free → cheap proxy → premium proxy →
  hosted unlocker.

## IP rotation

The single highest-leverage anti-bot lever. The reference design treats
the proxy provider as a pluggable strategy with a uniform interface.

### Free / cheap

- **`requests-ip-rotator`** — Tunnels HTTPS through **AWS API Gateway**;
  each request gets a fresh AWS egress IP. Free under the API Gateway
  free tier. **Best price/performance for low-volume scraping of
  IP-rate-limited APIs.** Limitations: AWS IP ranges are sometimes
  blocked; HTTPS only; not suitable when geo matters.
- **Tor via `stem`** — Free, anonymous, *slow*, and many sites preemptively
  block exit nodes. Last-resort fallback.
- **`proxybroker2` / public proxy lists** — Don't. Burn rate is huge and
  exit nodes are commonly hostile.

### Datacenter proxies (paid, cheap, often blocked)

- **Webshare**, **Proxy-Cheap**, **IPRoyal datacenter** — Cheap, fine for
  non-hardened targets.

### Residential / ISP / mobile proxies (paid, $$$, hard to block)

- **Bright Data** — Most features, highest cost. Sticky sessions, geo
  targeting, Web Unlocker, SERP API. Treat as ceiling tier.
- **Oxylabs** — Comparable to Bright Data. Better support for some.
- **Smartproxy / SOAX / NetNut / IPRoyal residential** — Mid-tier; good
  default for production scraping if AWS Gateway is too detectable.

### Rotation patterns we should support

- **Per-request rotation** — Each request gets a new IP.
- **Sticky session** — Same IP for N minutes (needed for sites with
  session cookies tied to IP).
- **Per-domain pool** — Domain A uses datacenter proxies, Domain B uses
  residential. Set by config.
- **Burn list** — Mark an IP as bad for a domain on 403/429/captcha;
  evict for a cooldown window.
- **Geo selection** — Pick exit country/city.

## Parsing

- **`selectolax`** — Lexbor-backed HTML parser. ~10x faster than
  BeautifulSoup, drop-in CSS selectors. Default.
- **`parsel`** — Scrapy's parser. XPath + CSS, ergonomic for nested
  extraction.
- **`lxml`** — Lower-level; reach for it when you need XPath features
  parsel doesn't expose.
- **Always sniff for JSON first.** `view-source:` and the network tab in
  DevTools will often show `__NEXT_DATA__`, GraphQL responses, or
  internal JSON APIs that bypass HTML parsing entirely. JSON endpoints
  are an order of magnitude more stable than DOM selectors.

## Cross-cutting helpers worth knowing

- **`tenacity`** — Retry decorators with backoff + jitter. Reference
  uses it.
- **`pyrate-limiter`** / **`aiolimiter`** — Token-bucket rate limiting
  per host.
- **`fake-useragent`** / **`user_agents`** — UA strings. Less useful
  than TLS fingerprinting but still expected.
- **`robotexclusionrulesparser`** / built-in `urllib.robotparser` —
  Robots.txt. Default-on, opt-out per job.
- **`w3lib`** — URL canonicalization (huge for dedupe).

## How to choose

Decision tree we apply per target:

1. Is there a public/JSON API or RSS/sitemap? Use it. Done.
2. Plain HTML, no anti-bot? `httpx` + `selectolax`.
3. TLS-fingerprint blocked? `curl_cffi`.
4. JS-rendered or Cloudflare Turnstile? `playwright-stealth`.
5. Still blocked? Add rotating residential proxies.
6. Still blocked? Hosted unlocker (vendor) tier.

Each step is a *separate fetcher implementation* behind the same
`Fetcher` protocol — see `reference/fetcher.py`.
