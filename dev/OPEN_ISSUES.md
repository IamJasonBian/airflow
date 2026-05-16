# Apache Airflow — Open Issues Snapshot

> Snapshot generated 2026-05-16. Sorted by last-updated, most-recent first.
> Source: https://github.com/apache/airflow/issues?q=is%3Aissue+is%3Aopen

---

## Critical / High Priority Bugs

| # | Title | Area | Priority |
|---|-------|------|----------|
| [#66853](https://github.com/apache/airflow/issues/66853) | API server OOMKill: task_instance row lock held during asset event emission under high concurrency | core | **critical** |
| [#66889](https://github.com/apache/airflow/issues/66889) | API write endpoints return opaque 500 when the database rejects a payload | API | high |
| [#66838](https://github.com/apache/airflow/issues/66838) | Improve `BaseCoordinator` interface to support pluggable communication channels | core / AIP-108 | high |
| [#66836](https://github.com/apache/airflow/issues/66836) | `JavaCoordinator`: Rename `bundles_folder`, accept `list[str]`, switch coordinator config to dict | core / AIP-108 | high |

---

## Bugs (needs-triage / lower priority)

| # | Title | Area |
|---|-------|------|
| [#67028](https://github.com/apache/airflow/issues/67028) | Dag processor error (metrics / helm-chart) | helm-chart, metrics |
| [#67027](https://github.com/apache/airflow/issues/67027) | KeycloakAuthManager returns 403 on `/api/v1/dags` despite valid SuperAdmin roles | API, auth |
| [#67025](https://github.com/apache/airflow/issues/67025) | Broken URLs to apache.org downloads in airflow-ctl docs (404) | documentation |
| [#66963](https://github.com/apache/airflow/issues/66963) | `BigQueryStreamingBufferEmptySensor` can falsely report an empty streaming buffer (metadata lag) | providers/google |
| [#66961](https://github.com/apache/airflow/issues/66961) | Provider triggers whose `serialize()` drops `__init__` parameters | providers, Triggerer |
| [#66959](https://github.com/apache/airflow/issues/66959) | UI: Calendar view renders failed runs in solid green, indistinguishable from success | UI |
| [#66877](https://github.com/apache/airflow/issues/66877) | `ExternalTaskSensor` can succeed early for task groups with NULL task states | providers/standard |
| [#66845](https://github.com/apache/airflow/issues/66845) | `get_async_connection` hard-codes `BaseHook.aget_connection`, bypassing subclass overrides | providers |
| [#66827](https://github.com/apache/airflow/issues/66827) | Not-in-use tags still present in the UI search bar | UI |

---

## Features & Improvements

| # | Title | Area |
|---|-------|------|
| [#67033](https://github.com/apache/airflow/issues/67033) | Add a Backend.AI provider package | providers |
| [#66987](https://github.com/apache/airflow/issues/66987) | Add `AzureBlobStorageDagBundle` | providers/azure |
| [#66947](https://github.com/apache/airflow/issues/66947) | Dag list page: show task state counts for the most recent Dag run | UI |
| [#66946](https://github.com/apache/airflow/issues/66946) | Dag list page: show total run state counts per Dag | UI |
| [#66944](https://github.com/apache/airflow/issues/66944) | Dag and task-level callbacks in the Go SDK | core / go-sdk |
| [#66943](https://github.com/apache/airflow/issues/66943) | E2E and Breeze coverage for the executable coordinator path (Go SDK) | core / dev-tools / go-sdk |
| [#66858](https://github.com/apache/airflow/issues/66858) | Helm Chart: `dag_bundle_config_list` changes roll every component (only dag-processor needs it) | helm-chart |
| [#66842](https://github.com/apache/airflow/issues/66842) | Wire async task state access for AIP-98 async tasks | core / async-operators |
| [#66837](https://github.com/apache/airflow/issues/66837) | Decouple Cadwyn (FastAPI/Starlette) hard dependencies from Task SDK | dependencies / AIP-108 |
| [#66818](https://github.com/apache/airflow/issues/66818) | Emit Stats counter when `DagRun.update_state` detects task deadlock | core, metrics |

---

## Good First Issues

| # | Title | Area |
|---|-------|------|
| [#66987](https://github.com/apache/airflow/issues/66987) | Add `AzureBlobStorageDagBundle` | providers/azure |
| [#66961](https://github.com/apache/airflow/issues/66961) | Fix provider triggers whose `serialize()` drops `__init__` parameters | providers, Triggerer |
| [#66839](https://github.com/apache/airflow/issues/66839) | Improve Databricks operators with query tags | providers/databricks |

---

## Summary by Area

| Area | Open Issues |
|------|-------------|
| providers | 7 |
| core | 6 |
| UI | 4 |
| API | 2 |
| helm-chart | 2 |
| AIP-108 / coordinator | 3 |
| documentation | 1 |
| dependencies | 1 |
