# Open PRs Snapshot — 2026-06-22

> Branch synced with `upstream/main` (apache/airflow). The fork has no issues;
> active work is tracked as open pull requests below.

**Total open PRs on fork:** 11  
**Synced at:** 2026-06-22

---

## Active Feature PRs (non-draft, open)

| # | Title | Branch | Note |
|---|-------|--------|------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add airflowctl monitor get-health command | `airflowctl-monitor-health` | Mirrors `GET /monitor/health`; generated help artifacts need CI regeneration |
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add airflowctl dagrun clear/update/delete | `airflowctl-dagrun-extensions` | 3 new DagRun mutating endpoints; integration tests intentionally excluded for destructive ops |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add airflowctl tasks list/get commands | `airflowctl-tasks-structural` | Mirrors read-only structural task definitions |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add airflowctl taskinstances list/get-tries/get-dependencies | `airflowctl-taskinstances-extensions` | Extends TI ops; based on #26 branch |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add airflowctl eventlogs commands | `airflowctl-eventlogs` | Read-only audit log: list + get |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add airflowctl dags get-source command | `airflowctl-dag-sources` | Mirrors `GET /dagSources/{dag_id}` |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support --map-index in airflowctl tasks state (CI test on fork) | `fix/airflowctl-taskinstances-integration-test` | Integration/CI validation branch |

## Draft / Sync PRs

| # | Title | Branch | Note |
|---|-------|--------|------|
| [#34](https://github.com/IamJasonBian/airflow/pull/34) | Sync from upstream/main + open issues snapshot (2026-06-21) | `claude/vibrant-thompson-2qkzeu` | Prior scheduled run — superseded by this one |
| [#33](https://github.com/IamJasonBian/airflow/pull/33) | Add automated open issues snapshot (2026-06-20) | `claude/vibrant-thompson-1rc2m7` | Prior scheduled run — superseded |
| [#25](https://github.com/IamJasonBian/airflow/pull/25) | Add sync and issue status summary to dev/ | `claude/vibrant-thompson-a5a1z3` | Prior scheduled run — superseded |
| [#24](https://github.com/IamJasonBian/airflow/pull/24) | dev: sync from upstream/main + open issues snapshot (2026-06-18) | `claude/vibrant-thompson-js0ned` | Prior scheduled run — superseded |

---

## Theme

All 7 non-draft PRs follow the same pattern: expanding `airflowctl` REST API
coverage by adding new `Operations` subclasses and auto-generated CLI subcommands.
A recurring blocker is that the **generated help-image artifacts**
(`airflow-ctl/docs/images/command_hashes.txt`, `output_main.svg`) cannot be
regenerated outside a Breeze/Docker environment — each PR notes they need a
`prek run capture-airflowctl-help` pass before merge.

## Next actions

1. Regenerate help artifacts for PRs #27–#32 via `prek run capture-airflowctl-help` in a Breeze environment.
2. Close stale draft PRs #24, #25, #33, #34 (superseded by this run's PR).
3. Review and merge open feature PRs once CI and help artifacts are green.
