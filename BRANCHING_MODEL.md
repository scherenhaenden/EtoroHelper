# Branching Model for EtoroHelper
> This document describes the Git branching model used in EtoroHelper, based on a simplified GitFlow adapted to the Magnetar Canonical Model.
---
## 1. Branch Types
| Branch | Purpose | Base Branch | Merge Target |
|--------|---------|------------|-------------|
| `master` | Immutable release line — production-ready code only | — | — |
| `develop` *(optional)* | Integration branch — aggregates completed features | `master` | `master` |
| `feature/<description>` | New functionality | `master` or `develop` | `master` or `develop` |
| `fix/<description>` | Bug corrections | `master` or `develop` | `master` or `develop` |
| `chore/<description>` | Maintenance, refactoring, tooling, documentation | `master` or `develop` | `master` or `develop` |
| `experiment/<description>` | Exploratory spikes (not guaranteed to merge) | `master` | `master` (if accepted) |
| `hotfix/<description>` | Critical production fixes | `master` | `master` (+ `develop` if active) |
---
## 2. Naming Convention
```
<type>/<short-description>
```
Examples:
- `feature/add-csv-export`
- `fix/stats-parser-esg-selector`
- `chore/apply-magnetar-model`
- `hotfix/blocker-selenium-crash`
- Use **lowercase** and **hyphens** only — no spaces, underscores, or uppercase.
- Keep descriptions **short and descriptive** (3–5 words max).
---
## 3. Workflow
### Starting Work
```bash
git checkout master
git pull origin master
git checkout -b feature/your-feature-name
```
### Before Merging
1. Rebase onto the latest `master` (or `develop`):
   ```bash
   git fetch origin
   git rebase origin/master
   ```
2. Ensure all tests pass locally: `uv run pytest`
3. Update `BITACORA.md` with a PR merge entry.
4. Update `STATUS.md` if milestone progress changed.
### Pull Request Rules
- PR title must reference the task ID: `[task-301] Apply Magnetar Canonical Model`
- PR description must include:
  - Task IDs affected
  - Summary of changes
  - Test evidence (or explanation of why manual testing was used)
- CI must be green before merge.
- At least one review (self-review acceptable for solo projects, documented in `BITACORA.md`).
---
## 4. `master` Branch Protection
- Direct pushes to `master` are **prohibited**.
- All changes arrive via Pull Request.
- Squash merges preferred to keep history linear.
- Every merge to `master` must have an associated `BITACORA.md` entry.
---
## 5. Hotfix Process
```bash
git checkout master
git pull origin master
git checkout -b hotfix/blocker-description
# ... fix ...
git push origin hotfix/blocker-description
# Open PR → merge to master → tag release
# Also merge to develop if develop branch is active
```
After merging a hotfix:
- Update `STATUS.md` immediately.
- Resolve the associated blocker in `BLOCKERS.md`.
- Log resolution in `BITACORA.md`.
