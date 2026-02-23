# Canonical Ruleset of EtoroHelper
> These rules codify the Magnetar standard. The entire project must comply with this ruleset unless a formal exception is documented in `BITACORA.md`.
---
## 1. Naming Conventions
| Entity | Convention | Example |
|--------|-----------|---------|
| **Repositories** | `magnetar-<domain>-<descriptor>` | `magnetar-finance-etorohelper` |
| **Branches** | `<type>/<short-description>` | `feature/add-csv-export` |
| **Tasks** | `kebab-case` with prefix | `task-201`, `task-parse-stats` |
| **Blockers** | `kebab-case` with prefix | `blocker-selenium-crash` |
| **YAML Keys** | `lower_snake_case` | `target_date`, `effort_pts` |
| **File Names** | Mirror canonical repository | `PLAN.md`, `BITACORA.md` |
### Valid Branch Types
- `feature` — New functionality
- `fix` — Bug corrections
- `chore` — Maintenance, refactoring, tooling
- `experiment` — Exploratory spikes
- `hotfix` — Critical production fixes
---
## 2. Required Files
Every EtoroHelper release must include all of the following. **Omission requires an explicit exemption logged in `BITACORA.md`.**
- `README.md`
- `PLAN.md`
- `BITACORA.md`
- `REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `RULES.md`
- `STATUS.md`
- `TESTING.md`
- `BLOCKERS.md`
- `BRANCHING_MODEL.md`
- `WIP_GUIDELINES.md`
- `CONTRIBUTING.md`
- `projects/etorohelper.project.yml`
---
## 3. Branching Conventions
| Branch | Rule |
|--------|------|
| `master` | Immutable release line. Merges require successful CI and documentation updates. |
| `develop` *(optional)* | Aggregates completed features before stabilisation. |
| `feature/*` | Originates from `master` or `develop`. Must be rebased before merging. |
| `hotfix/*` | Starts from `master`. Must trigger a `STATUS.md` update upon completion. |
- Every Pull Request must **reference the task IDs** it affects.
- Every Pull Request must include a **`BITACORA.md` entry** summarising the change.
---
## 4. Allowed Task States
| # | State | Description |
|---|-------|-------------|
| 1 | `planned` | Identified but not yet ready for work |
| 2 | `ready` | Refined, scoped, and ready to be started |
| 3 | `in_progress` | Actively being worked on |
| 4 | `in_review` | Work complete; awaiting review or approval |
| 5 | `blocked` | Cannot proceed due to an impediment |
| 6 | `done` | Accepted and merged |
### Allowed Transitions
```
planned → ready → in_progress → in_review → done
                       ↕
                   blocked
```
- `blocked` may transition back to `in_progress` once the blocker is resolved.
- Tasks must **not** skip states without a logged rationale in `BITACORA.md`.
---
## 5. Work-In-Progress (WIP) Constraints
- **WIP Limit:** Maximum **2** tasks in `in_progress` per individual or AI agent simultaneously.
- **Exceptions:** Exceeding the limit requires approval documented in `WIP_GUIDELINES.md` and `BITACORA.md`.
---
## 6. Blocker Lifecycle
1. **Discovery** — Log in `BLOCKERS.md` with: ID, description, severity (`low`/`medium`/`high`/`critical`), owner, and timestamp.
2. **Assessment** — Update risks in `STATUS.md`; note mitigation ideas in `BITACORA.md`.
3. **Escalation** — If not resolved within **1 business day**, escalate per the policy in `BLOCKERS.md`.
4. **Resolution** — Document solution steps in `BITACORA.md`; update blocker status to `resolved`.
5. **Retrospective** — Capture lessons learned in `BITACORA.md` under the `Discovery` category.
---
## 7. Documentation Discipline
| Document | Update Frequency |
|----------|-----------------|
| `BITACORA.md` | Every state change, decision, or exception — chronologically, newest first |
| `STATUS.md` | At least once per day or after each PR merge |
| `PLAN.md` | Whenever tasks change state or scope |
| `BLOCKERS.md` | Immediately upon blocker discovery or resolution |
---
## 8. AI Agent Responsibilities
- Parse `projects/etorohelper.project.yml` **before** taking any action.
- Do **not** open PRs without confirming the task state is `in_review`.
- Document **assumptions** in `BITACORA.md` when uncertain.
- Respect WIP limits and branching rules identically to human contributors.
---
## 9. Compliance and Enforcement
- **CI Validation:** Continuous Integration should validate the presence and basic structure of all required files on every PR.
- **Periodic Audits:** The project lead will conduct audits against this ruleset at every milestone completion.
- **Non-compliance:** Any deviation found in audit must be corrected within the next sprint and logged in `BITACORA.md`.
