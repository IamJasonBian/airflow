# Apache Airflow — Open Issues Summary

_Last updated: 2026-06-20 (automated routine)_

## Sync Status

Branch `claude/vibrant-thompson-1rc2m7` is **up to date** with `origin/main`
(HEAD: `e5f2af8e` — "Merge branch 'apache:main' into main").

The upstream `apache/airflow` repo is accessed through the fork's GitHub sync;
direct git fetch from `apache/airflow` is not available in this environment.

---

## Open Issues in `apache/airflow`

**Total open:** 1,154 issues  
_(30 most recently updated shown below as of 2026-06-20)_

### Bugs

| # | Title | Area | Priority | Updated |
|---|-------|------|----------|---------|
| [#68754](https://github.com/apache/airflow/issues/68754) | 'Task State Store' or 'Xcom' key is getting overlapped with expand/collapse details panel | UI | — | 2026-06-19 |
| [#68747](https://github.com/apache/airflow/issues/68747) | Editing task state store throws validation error | UI | — | 2026-06-19 |
| [#50708](https://github.com/apache/airflow/issues/50708) | Small memory leak from the dag-processor in Airflow 3.x | performance, core | — | 2026-06-19 |
| [#50334](https://github.com/apache/airflow/issues/50334) | Otel Metrics missing dag_ids | metrics, core | — | 2026-06-19 |
| [#51874](https://github.com/apache/airflow/issues/51874) | Recovering encrypted variables and connections after new installation | helm-chart | — | 2026-06-19 |
| [#48955](https://github.com/apache/airflow/issues/48955) | Dynamic generated Dag using JINJA template is not appearing in the Airflow UI | core | — | 2026-06-19 |
| [#47963](https://github.com/apache/airflow/issues/47963) | Problem with Rotation of Fernet Key | secrets, helm-chart | — | 2026-06-19 |
| [#50102](https://github.com/apache/airflow/issues/50102) | Can't select the desired dag version for a backfill dag run | core, backfill | — | 2026-06-19 |
| [#68732](https://github.com/apache/airflow/issues/68732) | Deadline never fires after non-deadline Dag edit due to orphaned deadline_alert | core | — | 2026-06-19 |
| [#68693](https://github.com/apache/airflow/issues/68693) | API server leaks a KubernetesExecutor multiprocessing.Manager process per worker when viewing RUNNING task logs | API, k8s | — | 2026-06-18 |
| [#68721](https://github.com/apache/airflow/issues/68721) | Backfill premature completion (confirmed on Airflow 3.2.2) | Scheduler, backfill | — | 2026-06-18 |
| [#68240](https://github.com/apache/airflow/issues/68240) | StackdriverRemoteLogIO: three bugs in AF3 supervisor context — empty labels, broken read filter, unguarded send crash | logging, google | — | 2026-06-18 |
| [#68683](https://github.com/apache/airflow/issues/68683) | KubernetesExecutor: self.completed adoption set is never drained, completed pods re-PATCHed every sync() loop | providers, k8s | **high** | 2026-06-18 |
| [#68483](https://github.com/apache/airflow/issues/68483) | Migration issue upgrading Airflow 3.1.8 to 3.2.2 | upgrade, db-migrations | — | 2026-06-18 |
| [#51840](https://github.com/apache/airflow/issues/51840) | run_after not respected when last DagRun is scheduled but not executed | Scheduler | — | 2026-06-18 |
| [#68699](https://github.com/apache/airflow/issues/68699) | Concurrent POST /api/v2/backfills causes HTTP 500 + partial data with SQLite metadata DB | MetaDB, API, backfill | — | 2026-06-18 |
| [#54474](https://github.com/apache/airflow/issues/54474) | ui_color is ignored for Taskgroup and custom operators in airflow 3.0.4 | core, UI | — | 2026-06-19 |

### Features / Enhancements

| # | Title | Area | Updated |
|---|-------|------|---------|
| [#66174](https://github.com/apache/airflow/issues/66174) | [AIP-94] airflowctl tasks: add state command _(good first issue)_ | CLI, airflow-ctl | 2026-06-19 |
| [#68402](https://github.com/apache/airflow/issues/68402) | [AIP-94] airflowctl command migration | CLI, airflow-ctl | 2026-06-19 |
| [#64278](https://github.com/apache/airflow/issues/64278) | Google Cloud Connection support for non-environmental proxy | providers, google | 2026-06-19 |
| [#53040](https://github.com/apache/airflow/issues/53040) | Improve filtering support in Airflow 3.x UI Views | UI | 2026-06-19 |
| [#50779](https://github.com/apache/airflow/issues/50779) | Add tab for asset groups and allow filtering for asset tags and URIs | UI | 2026-06-19 |
| [#54958](https://github.com/apache/airflow/issues/54958) | Add sticky callout bar for Dags and Task Instances needing review | UI | 2026-06-19 |
| [#39937](https://github.com/apache/airflow/issues/39937) | The graph should show the median task duration | UI | 2026-06-19 |
| [#63715](https://github.com/apache/airflow/issues/63715) | Add a time range selector for the Gantt view _(good first issue)_ | UI | 2026-06-19 |
| [#68532](https://github.com/apache/airflow/issues/68532) | Add an aggregate Dag schedule view: typical daily run times across all Dags | UI | 2026-06-18 |

### Meta / Docs / Tech Debt

| # | Title | Area | Updated |
|---|-------|------|---------|
| [#68751](https://github.com/apache/airflow/issues/68751) | Status of testing Providers that were prepared on June 19, 2026 | providers, testing | 2026-06-20 |
| [#63179](https://github.com/apache/airflow/issues/63179) | [DOCS] Helm Chart: Different Volumes/VolumeMount for each Celery Workers Sets | helm-chart, docs | 2026-06-19 |
| [#68374](https://github.com/apache/airflow/issues/68374) | [Tech Debt] Unit Test Isolation: Clean up Bundle and Team unit tests | core | 2026-06-18 |
| [#68757](https://github.com/apache/airflow/issues/68757) | Refactor: Migrate `os.path` to `pathlib.Path` in `file_processor_handler.py` | — | 2026-06-19 |

---

## Highlights

- **High-priority bug:** [#68683](https://github.com/apache/airflow/issues/68683) — KubernetesExecutor never drains its `completed` set, causing every completed pod to be re-PATCHed on every sync loop.
- **Active AIP-94 work:** Issues [#66174](https://github.com/apache/airflow/issues/66174) and [#68402](https://github.com/apache/airflow/issues/68402) track the `airflowctl` command migration; [#66174](https://github.com/apache/airflow/issues/66174) is a good first issue.
- **Good first issues:** [#66174](https://github.com/apache/airflow/issues/66174) (airflowctl task state command), [#63715](https://github.com/apache/airflow/issues/63715) (Gantt time range selector), [#50102](https://github.com/apache/airflow/issues/50102) (backfill dag version picker).
- **Provider testing status:** [#68751](https://github.com/apache/airflow/issues/68751) is the active tracking issue for the June 19 provider release test run.
- **UI cluster:** Multiple open UI enhancement requests around filtering, graph views, and asset browsing (#53040, #50779, #54958, #39937, #68532).
