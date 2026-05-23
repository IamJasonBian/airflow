# Open Issues & Fork Status

_Last updated: 2026-05-23_

## Sync status

| Item | Value |
|------|-------|
| Fork main HEAD | `940c5fd` — Merge PR #3 (Docs: Add pre-submit checks quick reference) |
| Upstream access | Blocked in this environment — fork is the only reachable remote |
| Open GitHub issues | **0** |

## Open draft PRs

Five draft PRs have accumulated across sessions, all targeting `main`:

| # | Branch | Title | Created | Notes |
|---|--------|--------|---------|-------|
| [#8](https://github.com/IamJasonBian/airflow/pull/8) | `claude/vibrant-thompson-12qL9` | Add open issues summary and sync status to dev/ | 2026-05-22 | Superseded by this PR |
| [#7](https://github.com/IamJasonBian/airflow/pull/7) | `claude/vibrant-thompson-5zWae` | Add open issues snapshot and pre-submit checks docs to dev/ | 2026-05-21 | Superseded; also carries pre-submit docs already in main via #3 |
| [#6](https://github.com/IamJasonBian/airflow/pull/6) | `claude/vibrant-thompson-GaTKc` | Add open issues snapshot to dev/ | 2026-05-19 | Superseded |
| [#5](https://github.com/IamJasonBian/airflow/pull/5) | `claude/vibrant-thompson-zvCHm` | Docs: Add pre-submit checks quick reference to PR guidelines | 2026-05-18 | Content already merged via PR #3 |
| [#4](https://github.com/IamJasonBian/airflow/pull/4) | `claude/vibrant-thompson-MgGIN` | Add open issues snapshot to dev/ | 2026-05-16 | Superseded |

**Recommended action:** close PRs #4–#8 (all superseded or already merged) and merge this one.

## Notes

- The `upstream` remote (`apache/airflow`) is not reachable from the managed sandbox; syncing
  must be done outside the sandbox or by pushing a synced `main` to the fork.
- There are no open GitHub issues to action.
