# Open Issues Snapshot — 2026-06-03

## Sync status

| Item | Value |
|------|-------|
| Snapshot date | 2026-06-03 |
| `origin/main` SHA | `ca4527d2` |
| Current branch | `claude/vibrant-thompson-fO00m` |
| Branch status | Up to date with `origin/main` |

## GitHub issues

**0 open issues** on `IamJasonBian/airflow`. Issues are tracked upstream at
`apache/airflow`; this fork does not carry its own issue backlog.

## Open draft PRs (action needed)

There are **15 stale draft PRs** from previous agent sessions, all doing this
same "sync + open issues summary" task. None have been merged or closed.

| PR | Title | Branch | Opened |
|----|-------|--------|--------|
| [#18](https://github.com/IamJasonBian/airflow/pull/18) | dev: update open issues snapshot (2026-06-02) | claude/vibrant-thompson-8IaXS | 2026-06-02 |
| [#17](https://github.com/IamJasonBian/airflow/pull/17) | Add open issues snapshot and sync fork main from upstream | claude/vibrant-thompson-JXOhx | 2026-06-01 |
| [#16](https://github.com/IamJasonBian/airflow/pull/16) | dev: update open issues snapshot (2026-05-31) | claude/vibrant-thompson-7kjuc | 2026-05-31 |
| [#15](https://github.com/IamJasonBian/airflow/pull/15) | Add open issues summary to dev/ | claude/vibrant-thompson-KUu0f | 2026-05-30 |
| [#14](https://github.com/IamJasonBian/airflow/pull/14) | Add session notes with sync status and open issues summary | claude/vibrant-thompson-vWFFJ | 2026-05-29 |
| [#13](https://github.com/IamJasonBian/airflow/pull/13) | dev: update open issues snapshot (2026-05-28) | claude/vibrant-thompson-6GvnU | 2026-05-28 |
| [#12](https://github.com/IamJasonBian/airflow/pull/12) | dev: update open issues snapshot (2026-05-27) | claude/vibrant-thompson-Xw6kR | 2026-05-27 |
| [#11](https://github.com/IamJasonBian/airflow/pull/11) | dev: update open issues snapshot (2026-05-25) | claude/vibrant-thompson-RNQWa | 2026-05-25 |
| [#10](https://github.com/IamJasonBian/airflow/pull/10) | dev: update open issues snapshot (2026-05-24) | claude/vibrant-thompson-aZ6wV | 2026-05-24 |
| [#9](https://github.com/IamJasonBian/airflow/pull/9)   | dev: update open issues snapshot (2026-05-23) | claude/vibrant-thompson-TOKPz | 2026-05-23 |
| [#8](https://github.com/IamJasonBian/airflow/pull/8)   | Add open issues summary and sync status to dev/ | claude/vibrant-thompson-12qL9 | 2026-05-22 |
| [#7](https://github.com/IamJasonBian/airflow/pull/7)   | Add open issues snapshot and pre-submit checks docs to dev/ | claude/vibrant-thompson-5zWae | 2026-05-21 |
| [#6](https://github.com/IamJasonBian/airflow/pull/6)   | Add open issues snapshot to dev/ | claude/vibrant-thompson-GaTKc | 2026-05-19 |
| [#5](https://github.com/IamJasonBian/airflow/pull/5)   | Docs: Add pre-submit checks quick reference to PR guidelines | claude/vibrant-thompson-zvCHm | 2026-05-18 |
| [#4](https://github.com/IamJasonBian/airflow/pull/4)   | Add open issues snapshot to dev/ | claude/vibrant-thompson-MgGIN | 2026-05-16 |

**Recommended action:** Close PRs #4–#17 as superseded. This PR (#19, once
opened) becomes the canonical snapshot going forward — or stop opening new PRs
for this task entirely and simply update this file in place on the branch.

## Notes

- The `upstream` remote (`apache/airflow`) is not reachable from the managed
  cloud environment. Syncing is done against `origin/main` (the fork's main
  branch, which is kept in sync via periodic merges from upstream).
- To add the upstream remote locally: `git remote add upstream https://github.com/apache/airflow.git`
