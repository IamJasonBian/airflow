# Apache Airflow — Open Issues Summary

**Snapshot date:** 2026-06-01  
**Total open issues:** 1,218  
**This snapshot covers:** 50 most recently updated issues

---

## By Area

### `area:core` — 18 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67801](https://github.com/apache/airflow/issues/67801) | 0 | Provide PgBouncer-safe defaults for the async metadata engine (asyncpg) |
| [#67797](https://github.com/apache/airflow/issues/67797) | 0 | Go-SDK: Coordinator-mode task failures never transition to UP_FOR_RETRY |
| [#66104](https://github.com/apache/airflow/issues/66104) | 32 | `dag_discovery_safe_mode` not scanning all files when set to False |
| [#67368](https://github.com/apache/airflow/issues/67368) | 8 | Clarify partition_key semantics across DagRun / AssetEvent / runtime |
| [#65505](https://github.com/apache/airflow/issues/65505) | 42 | Task-runner's venv/Popen subprocesses become orphans on heartbeat 409 (**priority:critical**) |

### `area:UI` — 8 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67852](https://github.com/apache/airflow/issues/67852) | 1 | Trigger Dag modal: two-column layout for params (label left, control right) |
| [#67851](https://github.com/apache/airflow/issues/67851) | 1 | Trigger Dag modal: long param names overflow modal width |
| [#67692](https://github.com/apache/airflow/issues/67692) | 2 | Type `asset_expression` on the API side so the UI doesn't cast through unknown |
| [#67647](https://github.com/apache/airflow/issues/67647) | 3 | UI: Unpin @chakra-ui/react (currently capped at ~3.34.0) (**good first issue**) |
| [#55734](https://github.com/apache/airflow/issues/55734) | 257 | Pool slot chart is misleading when deferred tasks don't consume slots (**good first issue**) |

### `area:providers` — 7 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67845](https://github.com/apache/airflow/issues/67845) | 1 | cncf.kubernetes: support kubernetes client 36.x — 35.x no_proxy regression |
| [#67643](https://github.com/apache/airflow/issues/67643) | 3 | KubernetesExecutor: Task stuck in queued state when using deprecated `executor_config` |
| [#66752](https://github.com/apache/airflow/issues/66752) | 19 | Create MSSQL connection lost schema field value |
| [#55368](https://github.com/apache/airflow/issues/55368) | 265 | EksPodOperator deferrable=true pause, restart and then wait until completion (**good first issue**) |
| [#24171](https://github.com/apache/airflow/issues/24171) | 1458 | Track SparkSubmitHook Yarn Cluster application with Yarn CLI (**good first issue**) |

### `area:API` — 6 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67799](https://github.com/apache/airflow/issues/67799) | 0 | Migrate API endpoints from sync to async DB sessions |
| [#67695](https://github.com/apache/airflow/issues/67695) | 2 | Bug in Patching DagRun + Mark dag as `success` and `failed` have different behavior |
| [#66713](https://github.com/apache/airflow/issues/66713) | 20 | Heartbeat 404 "Task Instance not found" after ~12h run |
| [#52280](https://github.com/apache/airflow/issues/52280) | 339 | Redesign Databricks Workflow Repair Functionality for Airflow 3 Compatibility |
| [#10937](https://github.com/apache/airflow/issues/10937) | 2085 | Automate reference doc creation for stable API permissions (**good first issue**) |

### `area:helm-chart` — 5 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67837](https://github.com/apache/airflow/issues/67837) | 1 | Publish Helm Chart as OCI Artifact |
| [#67821](https://github.com/apache/airflow/issues/67821) | 1 | Status of testing of Apache Airflow Helm Chart 1.22.0rc1 |
| [#67814](https://github.com/apache/airflow/issues/67814) | 0 | Add boolean option to Helm Chart for splitting api-server |
| [#61452](https://github.com/apache/airflow/issues/61452) | 116 | Add support for Kubernetes Gateway API (HTTPRoute) in Helm Chart |
| [#66858](https://github.com/apache/airflow/issues/66858) | 18 | Helm Chart: dag_bundle_config_list changes roll every Airflow component unnecessarily |

### `area:Scheduler` — 2 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67287](https://github.com/apache/airflow/issues/67287) | 10 | Race condition between scheduler processing events and trigger completion — queuing |
| [#41036](https://github.com/apache/airflow/issues/41036) | 674 | Tasks running when a Dag run reaches its timeout should optionally support termination (**good first issue**) |

### `area:CLI` — 2 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67484](https://github.com/apache/airflow/issues/67484) | 6 | Bulk-clear path for `airflow dags clear` to avoid N transactions |
| [#49074](https://github.com/apache/airflow/issues/49074) | 416 | `airflow tasks run` CLI creates a kubernetesJobWatcher when running with Celery executor |

---

## By Kind

### `kind:bug` — 22 issues (top 5 most recent)
| # | Age (days) | Title |
|---|-----------|-------|
| [#67851](https://github.com/apache/airflow/issues/67851) | 1 | Trigger Dag modal: long param names overflow modal width |
| [#67845](https://github.com/apache/airflow/issues/67845) | 1 | cncf.kubernetes: support kubernetes client 36.x |
| [#67801](https://github.com/apache/airflow/issues/67801) | 0 | Provide PgBouncer-safe defaults for the async metadata engine (asyncpg) |
| [#67797](https://github.com/apache/airflow/issues/67797) | 0 | Go-SDK: Coordinator-mode task failures never transition to UP_FOR_RETRY |
| [#66104](https://github.com/apache/airflow/issues/66104) | 32 | `dag_discovery_safe_mode` not scanning all files when set to False |

### `kind:feature` — 22 issues (top 5 most recent)
| # | Age (days) | Title |
|---|-----------|-------|
| [#67852](https://github.com/apache/airflow/issues/67852) | 1 | Trigger Dag modal: two-column layout for params |
| [#67841](https://github.com/apache/airflow/issues/67841) | 1 | Add default parameter to `get` methods? |
| [#67837](https://github.com/apache/airflow/issues/67837) | 1 | Publish Helm Chart as OCI Artifact |
| [#67814](https://github.com/apache/airflow/issues/67814) | 0 | Add boolean option to Helm Chart for splitting api-server |
| [#67799](https://github.com/apache/airflow/issues/67799) | 0 | Migrate API endpoints from sync to async DB sessions |

### `kind:documentation` — 3 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67706](https://github.com/apache/airflow/issues/67706) | 2 | Add guidance on when to use ResumableMixin vs deferrable operators |
| [#65782](https://github.com/apache/airflow/issues/65782) | 37 | Documentation for task and asset states |
| [#10937](https://github.com/apache/airflow/issues/10937) | 2085 | Automate reference doc creation for stable API permissions |

---

## By Provider

| Provider | Count | Top issue |
|---|---|---|
| `provider:cncf-kubernetes` | 2 | [#67845](https://github.com/apache/airflow/issues/67845) — kubernetes client 36.x support |
| `provider:amazon` | 2 | [#55368](https://github.com/apache/airflow/issues/55368) — EksPodOperator deferrable restart |
| `provider:databricks` | 1 | [#52280](https://github.com/apache/airflow/issues/52280) — Databricks Workflow Repair for AF3 |
| `provider:microsoft-mssql` | 1 | [#66752](https://github.com/apache/airflow/issues/66752) — MSSQL connection lost schema field |
| `provider:apache-spark` | 1 | [#24171](https://github.com/apache/airflow/issues/24171) — SparkSubmitHook Yarn Cluster tracking |
| `provider:celery` | 1 | [#49074](https://github.com/apache/airflow/issues/49074) — `airflow tasks run` creates kubernetesJobWatcher |
| `provider:postgres` | 1 | [#67801](https://github.com/apache/airflow/issues/67801) — PgBouncer-safe asyncpg defaults |

---

## AIP-108 (Coordinator / Multi-SDK) — 2 issues
| # | Age (days) | Title |
|---|-----------|-------|
| [#67797](https://github.com/apache/airflow/issues/67797) | 0 | Go-SDK: Coordinator-mode task failures never transition to UP_FOR_RETRY |
| [#67798](https://github.com/apache/airflow/issues/67798) | 0 | Java SDK: Coordinator-mode task failures never transition to UP_FOR_RETRY |

---

## Good First Issues — 8 total
| # | Age (days) | Area | Title |
|---|-----------|------|-------|
| [#67647](https://github.com/apache/airflow/issues/67647) | 3 | area:UI | UI: Unpin @chakra-ui/react (capped at ~3.34.0) |
| [#63503](https://github.com/apache/airflow/issues/63503) | 79 | area:core, area:metrics | Metric `queued_duration` missing |
| [#55734](https://github.com/apache/airflow/issues/55734) | 257 | area:core, area:UI | Pool slot chart misleading for deferred tasks |
| [#55368](https://github.com/apache/airflow/issues/55368) | 265 | provider:amazon | EksPodOperator deferrable=true pause/restart |
| [#41036](https://github.com/apache/airflow/issues/41036) | 674 | area:Scheduler | Dag run timeout: optionally terminate running tasks |
| [#26438](https://github.com/apache/airflow/issues/26438) | 1353 | area:core | Kerberos: switch MIT to Heimdal |
| [#24171](https://github.com/apache/airflow/issues/24171) | 1458 | area:providers | Track SparkSubmitHook Yarn Cluster with Yarn CLI |
| [#10937](https://github.com/apache/airflow/issues/10937) | 2085 | area:API | Automate reference docs for stable API permissions |

---

## Priority-Tagged Issues — 5 total
| # | Priority | Age (days) | Title |
|---|----------|-----------|-------|
| [#65505](https://github.com/apache/airflow/issues/65505) | **critical** | 42 | Task-runner venv/Popen subprocesses become orphans on heartbeat 409 |
| [#66936](https://github.com/apache/airflow/issues/66936) | **high** | 17 | Refactor ExecutableCoordinator interface (on hold) |
| [#66796](https://github.com/apache/airflow/issues/66796) | medium | 19 | `SerializedDagModel.get_count()` should raise on None scalar |
| [#63503](https://github.com/apache/airflow/issues/63503) | upgrade_to_airflow3 | 79 | Metric `dag.dag_id.task_id.queued_duration` missing |
| [#67801](https://github.com/apache/airflow/issues/67801) | low | 0 | PgBouncer-safe defaults for asyncpg |

---

## Notes

- Snapshot covers the **50 most-recently-updated** open issues out of 1,218 total — over-represents active/fresh issues.
- **17 of 50** recent issues are tagged `needs-triage`.
- **priority:critical** issue [#65505](https://github.com/apache/airflow/issues/65505) (orphan subprocesses on heartbeat 409) is 42 days old and still open.
- Both AIP-108 SDK issues ([#67797](https://github.com/apache/airflow/issues/67797) Go, [#67798](https://github.com/apache/airflow/issues/67798) Java) are brand new and describe the same retry-transition bug across languages.
