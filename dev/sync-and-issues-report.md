# Sync & Issues Report — 2026-06-13

## Sync status

Branch `claude/vibrant-thompson-vztqtw` has been merged with `upstream/main`
(apache/airflow) and pushed to `origin`.

- **Before sync:** `ca4527d2` (was 351 commits behind upstream)
- **After sync:** current upstream HEAD
- **Commits merged:** 351 new upstream commits

**Note:** The repo was missing the `upstream` remote (per `CLAUDE.md` convention,
`upstream` should point to `apache/airflow`; `origin` should point to the fork).
The remote was added during this run:

```bash
git remote add upstream https://github.com/apache/airflow.git
```

Re-run `git remote -v` to confirm the setup persists in future sessions, or add
it to the environment setup script if the container is ephemeral.

## Selected highlights from the 351 merged commits

### Features / AIPs
- `AIP-76`: Hold Dag run until all upstream partitions arrive; forward fan-out via `Window` (#64571, #67475)
- `AIP-103`: Task and Asset Store UI, docs, store-write attribution, `awaiting_input` state for Human-in-the-loop (#67292, #67299, #68028)
- `AIP-94`: CLI `airflowctl` client and adoption in existing commands (#68175)
- `FanOutMapper`, `FixedKeyMapper`, `SegmentWindow` for categorical asset-partition rollup (#67716, #66030)
- `Add ExecutableCoordinator` for self-contained Dag bundles (#67161)
- Go-SDK: coordinator-mode runtime, bundle packing, Go task authoring guide (#67318, #67156, #68223)
- Java SDK: final wire-up, publish config, e2e test, ADRs (#67826, #68016, #67956)
- `ResumableJobMixin` crash recovery (YARN cluster mode, SparkSubmitOperator) (#68213, #67473)
- ClickHouse provider added (#67080)
- Redis client self-identification (#61866)
- Amazon Bedrock AgentCore Runtime operators (#67984)

### Fixes
- Scheduler crash on non-ASCII Dag names with OTel metrics (#68023)
- Scheduler crash from KubernetesExecutor completed-pod adoption (#67850)
- Scheduler crashloop when last task instance predates Dag versioning (#68253)
- `none_failed_min_one_success` trigger rule (#67873)
- `airflow dags clear` clearing the wrong day for non-UTC partitioned timetables (#67717)
- Revert: Task SDK Stats explicit initialization in API server lifespan (#68481)
- Return 422 on DB-rejected API payloads (#66888)
- Fix secrets backends breaking on Airflow 3.2 (#68302)
- Fix upstream map index resolution after placeholder expansion (#59691 then reverted #68418)

### Infrastructure / Perf
- Dag file-queue dedup O(N²) → O(N) with OrderedDict (#67750)
- Bulk Dag run clear / mark-success/failed UI endpoints (#67846, #67948, #66888)
- Postgres `execute_values` for bulk inserts (#68207)
- Indexes on `dag_run.created_dag_version_id` and `task_instance.dag_version_id` (#64818)

### Multi-team
- Consumer team asset filtering (API + UI) (#68034, #68025)
- `allow_consumer_teams` / `allow_global_consumers` on `TaskOutletAssetReference` (#67730)
- Team-name support in pool CLI (#68110)

## Open issues on fork (iamjasonbian/airflow)

**0 open issues.** (Issues on the canonical `apache/airflow` repo are out of
scope for this fork's issue tracker; file upstream issues at
https://github.com/apache/airflow/issues.)
