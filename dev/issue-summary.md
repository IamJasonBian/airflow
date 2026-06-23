# Fork PR Summary — 2026-06-23

Branch synced with `origin/main` at `384f6505` ("Merge branch 'apache:main' into main").

---

## Open PRs (12 total)

### Ready for review (non-draft)

| # | Title | Branch |
|---|-------|--------|
| [#32](https://github.com/IamJasonBian/airflow/pull/32) | Add airflowctl monitor get-health command | `airflowctl-monitor-health` |
| [#30](https://github.com/IamJasonBian/airflow/pull/30) | Add airflowctl tasks list/get commands | `airflowctl-tasks-structural` |

### Feature PRs (draft)

| # | Title | Branch | Notes |
|---|-------|--------|-------|
| [#31](https://github.com/IamJasonBian/airflow/pull/31) | Add airflowctl dagrun clear/update/delete | `airflowctl-dagrun-extensions` | dry-run vs full response handled |
| [#29](https://github.com/IamJasonBian/airflow/pull/29) | Add airflowctl taskinstances list/get-tries/get-dependencies | `airflowctl-taskinstances-extensions` | based on #26 branch |
| [#28](https://github.com/IamJasonBian/airflow/pull/28) | Add airflowctl eventlogs commands | `airflowctl-eventlogs` | list + get |
| [#27](https://github.com/IamJasonBian/airflow/pull/27) | Add airflowctl dags get-source command | `airflowctl-dag-sources` | |
| [#26](https://github.com/IamJasonBian/airflow/pull/26) | Support --map-index in airflowctl tasks state | `fix/airflowctl-taskinstances-integration-test` | integration test CI branch |

### Stale scheduled-run PRs (safe to close)

These were created by automated routine runs and have been superseded:

| # | Title |
|---|-------|
| [#35](https://github.com/IamJasonBian/airflow/pull/35) | Sync from upstream/main + open PR snapshot (2026-06-22) |
| [#34](https://github.com/IamJasonBian/airflow/pull/34) | Sync from upstream/main + open issues snapshot (2026-06-21) |
| [#33](https://github.com/IamJasonBian/airflow/pull/33) | Add automated open issues summary (2026-06-20) |
| [#25](https://github.com/IamJasonBian/airflow/pull/25) | Add sync and issue status summary to dev/ |
| [#24](https://github.com/IamJasonBian/airflow/pull/24) | dev: sync from upstream/main + open issues snapshot (2026-06-18) |

---

## Recurring blocker

All 7 feature PRs are blocked from merging by missing generated help-image artifacts. Before any can merge, run:

```bash
prek run capture-airflowctl-help
```

This requires a Breeze/Docker environment and regenerates `airflow-ctl/docs/images/command_hashes.txt` and `output_main.svg`.

---

## Notes

- The fork has **0 open GitHub Issues** — issues live on [apache/airflow](https://github.com/apache/airflow/issues).
- All feature PRs expand `airflowctl` REST API v2 coverage following the pattern from apache/airflow#66509.
- #29 (`taskinstances list/get-tries/get-dependencies`) is based on #26's branch rather than `main` — it needs rebasing once #26 merges.
