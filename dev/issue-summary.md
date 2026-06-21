# Apache Airflow — Open Issues Snapshot

**Date:** 2026-06-21
**Total open issues (apache/airflow):** 1,154
**Branch:** `claude/vibrant-thompson-2qkzeu` — synced with `upstream/main` (merged 3 commits)

---

## Priority / High-Signal

| # | Title | Labels |
|---|-------|--------|
| [#68683](https://github.com/apache/airflow/issues/68683) | KubernetesExecutor: `self.completed` adoption set is never drained, completed pods accumulate | **priority:high**, kind:bug, provider:cncf-kubernetes |
| [#68693](https://github.com/apache/airflow/issues/68693) | API server leaks a KubernetesExecutor multiprocessing.Manager process per worker | kind:bug, area:API, provider:cncf-kubernetes |
| [#68796](https://github.com/apache/airflow/issues/68796) | AirflowRuntimeVaryingValueChecker misses runtime-varying values in tasks after n… | kind:bug, area:core |
| [#68794](https://github.com/apache/airflow/issues/68794) | MetastoreBackend.cleanup() ignores default_retention_days — task state rows without TTL never cleaned | kind:bug, area:core |
| [#68721](https://github.com/apache/airflow/issues/68721) | Backfill premature completion (confirmed on Airflow 3.2.2) | kind:bug, area:Scheduler, area:backfill |
| [#68732](https://github.com/apache/airflow/issues/68732) | Deadline never fires after non-deadline Dag edit due to orphaned deadline_alert | kind:bug, area:core |

---

## Good First Issues

| # | Title | Labels |
|---|-------|--------|
| [#68382](https://github.com/apache/airflow/issues/68382) | Connection port field does not validate that the value is a valid port number | kind:bug, good first issue, area:core |
| [#59093](https://github.com/apache/airflow/issues/59093) | XCom.get_value() via SDK fails in extra link plugin with SUPERVISOR_COMMS ImportError | kind:bug, good first issue, area:core |
| [#50102](https://github.com/apache/airflow/issues/50102) | Can't select the desired dag version for a backfill dag run | kind:bug, good first issue, area:core, area:backfill |
| [#59840](https://github.com/apache/airflow/issues/59840) | Remove export functionality from UI / Public API | kind:feature, good first issue, area:API, area:UI |
| [#63715](https://github.com/apache/airflow/issues/63715) | Add a time range selector for the Gantt view | good first issue, kind:feature, area:UI |
| [#51598](https://github.com/apache/airflow/issues/51598) | Airflow Databricks Operator Task Group Launch Task Not Properly Waiting for Upstream | kind:bug, good first issue, provider:databricks |
| [#55368](https://github.com/apache/airflow/issues/55368) | EksPodOperator deferrable=true pause, restart and then wait until completion | kind:bug, good first issue, provider:amazon |
| [#66174](https://github.com/apache/airflow/issues/66174) | [AIP-94] airflowctl tasks: add state command | kind:feature, good first issue, area:airflow-ctl |

---

## Bugs (recently updated)

| # | Title | Updated |
|---|-------|---------|
| [#68790](https://github.com/apache/airflow/issues/68790) | Exception type too broad in error handling | 2026-06-21 |
| [#68747](https://github.com/apache/airflow/issues/68747) | Editing task state store throws validation error | 2026-06-20 |
| [#68699](https://github.com/apache/airflow/issues/68699) | Concurrent POST /api/v2/backfills causes HTTP 500 + partial data with SQLite metadata DB | 2026-06-18 |
| [#68483](https://github.com/apache/airflow/issues/68483) | Migration issue upgrading Airflow 3.1.8 to 3.2.2 | 2026-06-18 |
| [#68240](https://github.com/apache/airflow/issues/68240) | StackdriverRemoteLogIO: three bugs in AF3 supervisor context — empty labels, broken format, missing fields | 2026-06-18 |
| [#50708](https://github.com/apache/airflow/issues/50708) | Small memory leak from the dag-processor in Airflow 3.x | 2026-06-19 |
| [#47963](https://github.com/apache/airflow/issues/47963) | Problem with Rotation of Fernet Key | 2026-06-20 |
| [#51840](https://github.com/apache/airflow/issues/51840) | run_after not respected when last DagRun is scheduled but not executed | 2026-06-18 |

---

## Features & Improvements (recently updated)

| # | Title | Area |
|---|-------|------|
| [#68402](https://github.com/apache/airflow/issues/68402) | [AIP-94] airflowctl command migration | area:airflow-ctl |
| [#68532](https://github.com/apache/airflow/issues/68532) | Add an aggregate Dag schedule view: typical daily run times across all Dags | area:UI |
| [#53040](https://github.com/apache/airflow/issues/53040) | Improve filtering support in Airflow 3.x UI Views | area:UI |
| [#61159](https://github.com/apache/airflow/issues/61159) | Save tables columns configuration | area:UI |
| [#55956](https://github.com/apache/airflow/issues/55956) | Asset event scheduling - introduce max_asset_events parameter | area:data-aware-scheduling |
| [#64278](https://github.com/apache/airflow/issues/64278) | Google Cloud Connection support for non-environmental proxy | provider:google |
| [#61430](https://github.com/apache/airflow/issues/61430) | Kubernetes best practices and Helm support for API server rollout restarts | area:helm-chart |

---

## Full List (50 most recently updated, of 1,154 total)

| # | Title | Labels | Updated |
|---|-------|--------|---------|
| [#51598](https://github.com/apache/airflow/issues/51598) | Airflow Databricks Operator Task Group Launch Task Not Properly Waiting for Upstream | kind:bug, area:providers, good first issue, provider:databricks | 2026-06-21 |
| [#55368](https://github.com/apache/airflow/issues/55368) | EksPodOperator deferrable=true pause, restart and then wait until completion | kind:bug, provider:amazon, area:providers, good first issue, pending-response | 2026-06-21 |
| [#68751](https://github.com/apache/airflow/issues/68751) | Status of testing Providers that were prepared on June 19, 2026 | area:providers, kind:meta, testing status | 2026-06-21 |
| [#68796](https://github.com/apache/airflow/issues/68796) | AirflowRuntimeVaryingValueChecker misses runtime-varying values in tasks | kind:bug, area:core, needs-triage | 2026-06-21 |
| [#68794](https://github.com/apache/airflow/issues/68794) | MetastoreBackend.cleanup() ignores default_retention_days | kind:bug, area:core | 2026-06-21 |
| [#68532](https://github.com/apache/airflow/issues/68532) | Add an aggregate Dag schedule view: typical daily run times across all Dags | kind:feature, area:UI | 2026-06-21 |
| [#68790](https://github.com/apache/airflow/issues/68790) | Exception type too broad in error handling | kind:bug, area:core | 2026-06-21 |
| [#59093](https://github.com/apache/airflow/issues/59093) | XCom.get_value() via SDK fails in extra link plugin with SUPERVISOR_COMMS ImportError | kind:bug, good first issue, area:core | 2026-06-21 |
| [#68757](https://github.com/apache/airflow/issues/68757) | Refactor: Migrate os.path to pathlib.Path in file_processor_handler.py | _(none)_ | 2026-06-21 |
| [#68747](https://github.com/apache/airflow/issues/68747) | Editing task state store throws validation error | kind:bug, area:core, area:UI, affected_version:3.3.0beta | 2026-06-20 |
| [#47963](https://github.com/apache/airflow/issues/47963) | Problem with Rotation of Fernet Key | kind:bug, area:secrets, area:helm-chart, pending-response | 2026-06-20 |
| [#66174](https://github.com/apache/airflow/issues/66174) | [AIP-94] airflowctl tasks: add state command | area:CLI, kind:feature, good first issue, area:airflow-ctl | 2026-06-19 |
| [#68402](https://github.com/apache/airflow/issues/68402) | [AIP-94] airflowctl command migration | area:CLI, kind:feature, kind:meta, area:airflow-ctl | 2026-06-19 |
| [#64278](https://github.com/apache/airflow/issues/64278) | Google Cloud Connection support for non-environmental proxy | provider:google, area:providers, kind:feature | 2026-06-19 |
| [#68754](https://github.com/apache/airflow/issues/68754) | 'Task State Store' or 'Xcom' key is getting overlapped with expand/collapse details | kind:bug, area:UI, needs-triage | 2026-06-19 |
| [#63715](https://github.com/apache/airflow/issues/63715) | Add a time range selector for the Gantt view | good first issue, type:new-feature, area:UI | 2026-06-19 |
| [#54474](https://github.com/apache/airflow/issues/54474) | ui_color is ignored for Taskgroup and custom operators in airflow 3.0.4 | area:core, area:UI, affected_version:3.0 | 2026-06-19 |
| [#48955](https://github.com/apache/airflow/issues/48955) | Dynamic generated Dag using JINJA template is not appearing in the Airflow UI | kind:bug, pending-response, area:core | 2026-06-19 |
| [#63179](https://github.com/apache/airflow/issues/63179) | [DOCS] Helm Chart: Different Volumes/VolumeMount for each Celery Workers Sets | area:helm-chart, kind:documentation | 2026-06-19 |
| [#50708](https://github.com/apache/airflow/issues/50708) | Small memory leak from the dag-processor in Airflow 3.x | kind:bug, area:performance, area:core, affected_version:3.0 | 2026-06-19 |
| [#50334](https://github.com/apache/airflow/issues/50334) | Otel Metrics missing dag_ids | kind:bug, area:metrics, area:core, needs-triage | 2026-06-19 |
| [#51874](https://github.com/apache/airflow/issues/51874) | Recovering encrypted variables and connections after new installation | kind:bug, area:helm-chart, needs-triage | 2026-06-19 |
| [#53040](https://github.com/apache/airflow/issues/53040) | Improve filtering support in Airflow 3.x UI Views | kind:feature, kind:meta, area:UI | 2026-06-19 |
| [#50779](https://github.com/apache/airflow/issues/50779) | Add tab for asset groups and allow filtering for asset tags and URIs | kind:feature, area:UI | 2026-06-19 |
| [#54958](https://github.com/apache/airflow/issues/54958) | Add sticky callout bar for Dags and Task Instances needing review | kind:feature, area:UI | 2026-06-19 |
| [#39937](https://github.com/apache/airflow/issues/39937) | The graph should show the median task duration | kind:feature, area:UI | 2026-06-19 |
| [#50102](https://github.com/apache/airflow/issues/50102) | Can't select the desired dag version for a backfill dag run | kind:bug, good first issue, area:core, area:backfill | 2026-06-19 |
| [#68732](https://github.com/apache/airflow/issues/68732) | Deadline never fires after non-deadline Dag edit due to orphaned deadline_alert | kind:bug, area:core, needs-triage | 2026-06-19 |
| [#68693](https://github.com/apache/airflow/issues/68693) | API server leaks a KubernetesExecutor multiprocessing.Manager process per worker | kind:bug, area:API, provider:cncf-kubernetes, needs-triage | 2026-06-18 |
| [#68374](https://github.com/apache/airflow/issues/68374) | [Tech Debt] Unit Test Isolation: Clean up Bundle and Team unit tests | area:core | 2026-06-18 |
| [#68721](https://github.com/apache/airflow/issues/68721) | Backfill premature completion (confirmed on Airflow 3.2.2) | kind:bug, area:Scheduler, area:core, area:backfill | 2026-06-18 |
| [#68240](https://github.com/apache/airflow/issues/68240) | StackdriverRemoteLogIO: three bugs in AF3 supervisor context | kind:bug, provider:google, area:logging | 2026-06-18 |
| [#68683](https://github.com/apache/airflow/issues/68683) | KubernetesExecutor: self.completed adoption set is never drained, completed pods accumulate | kind:bug, area:providers, **priority:high**, provider:cncf-kubernetes | 2026-06-18 |
| [#68483](https://github.com/apache/airflow/issues/68483) | Migration issue upgrading Airflow 3.1.8 to 3.2.2 | kind:bug, area:upgrade, needs-triage, area:db-migrations | 2026-06-18 |
| [#51840](https://github.com/apache/airflow/issues/51840) | run_after not respected when last DagRun is scheduled but not executed | kind:bug, area:Scheduler | 2026-06-18 |
| [#68699](https://github.com/apache/airflow/issues/68699) | Concurrent POST /api/v2/backfills causes HTTP 500 + partial data with SQLite metadata DB | kind:bug, area:MetaDB, area:API, area:backfill | 2026-06-18 |
| [#68382](https://github.com/apache/airflow/issues/68382) | Connection port field does not validate that the value is a valid port number | kind:bug, good first issue, area:core | 2026-06-18 |
| [#59840](https://github.com/apache/airflow/issues/59840) | Remove export functionality from UI / Public API | kind:feature, good first issue, area:API, area:UI | 2026-06-18 |
| [#61430](https://github.com/apache/airflow/issues/61430) | Kubernetes best practices and Helm support for API server rollout restarts | area:helm-chart, kind:documentation, kind:meta | 2026-06-18 |
| [#61159](https://github.com/apache/airflow/issues/61159) | Save tables columns configuration | kind:feature, area:UI | 2026-06-18 |
| [#59838](https://github.com/apache/airflow/issues/59838) | Consistent approach for sensitive value masking in CLIs | area:CLI, area:API, kind:meta | 2026-06-18 |
| [#55956](https://github.com/apache/airflow/issues/55956) | Asset event scheduling - introduce max_asset_events parameter | kind:feature, area:data-aware-scheduling | 2026-06-18 |
| [#43822](https://github.com/apache/airflow/issues/43822) | Include deferral in Task Instance Duration monitor | kind:feature, area:UI | 2026-06-18 |
| [#44376](https://github.com/apache/airflow/issues/44376) | Provide users choice of timezone to FileTaskHandler, for log timestamp formatting | area:logging, kind:feature, area:UI | 2026-06-18 |
| [#56486](https://github.com/apache/airflow/issues/56486) | Use UI snapshot testing to generate docs screenshots | kind:documentation, kind:meta, area:UI | 2026-06-18 |
| [#41312](https://github.com/apache/airflow/issues/41312) | Add Event Log summary to Task/Dag Overview tabs | kind:feature, priority:low, area:UI | 2026-06-18 |
| [#51163](https://github.com/apache/airflow/issues/51163) | More concise error message in the api-server log when execution_api_server_url is misconfigured | kind:feature, area:API, area:UI | 2026-06-18 |
| [#48887](https://github.com/apache/airflow/issues/48887) | Add automated detection of when Execution API migration is missing | area:API, area:CI | 2026-06-18 |
| [#44354](https://github.com/apache/airflow/issues/44354) | Move dag-level callbacks to worker | area:task-execution-interface-aip72 | 2026-06-18 |
| [#43439](https://github.com/apache/airflow/issues/43439) | Determine if including try_number in the UniqueConstraint improves index efficiency | area:performance, area:task-execution-interface-aip72 | 2026-06-18 |
