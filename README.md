# Canonical Project Model of EtoroHelper

> This project follows the **Magnetar Canonical Project Model** standard for documentation, planning, and governance.

---

## Purpose

**EtoroHelper** exists to automate the extraction, parsing, and organisation of data from the eToro social trading platform. It solves the problem of manual, error-prone data collection by providing a reproducible pipeline that downloads user profiles, portfolios, and statistics and converts them into structured JSON and Markdown outputs for easy analysis and reporting.

This repository adheres to the Magnetar standard for documentation, planning, and governance — ensuring every collaborator (human or AI) has a single source of truth for project state, decisions, and progress.

---

## How to Use This Repository

1. **Clone the canonical model** — `git clone <repo-url>` and explore the root-level documentation files.
2. **Copy and fill out the project YAML** — Use `projects/_template.project.yml` as your starting point; replace all placeholder values with project-specific data.
3. **Replicate the required documentation set** — Ensure all files listed in the *Project Contents* table exist and are populated.
4. **Follow the WIP, branching, and blocker rules** — Read `WIP_GUIDELINES.md`, `BRANCHING_MODEL.md`, and `RULES.md` before opening any branch or PR.
5. **Consult the example project** — The `example/` directory provides reference input/output to resolve questions about expected behaviour.

---

## Project Contents

| File | Purpose |
|------|---------|
| `PLAN.md` | Project tasks & milestones — the single source of truth for scope and progress |
| `BITACORA.md` | Chronological logbook — immutable record of decisions, state changes, and events |
| `REQUIREMENTS.md` | Functional & non-functional specifications |
| `ARCHITECTURE.md` | System/module structure and key design decisions |
| `RULES.md` | Naming conventions & workflow standards |
| `STATUS.md` | Health summary & progress statistics |
| `TESTING.md` | Test coverage, strategy, and reporting rules |
| `BLOCKERS.md` | Documented blockers & escalation paths |
| `BRANCHING_MODEL.md` | Git branching model and PR governance |
| `WIP_GUIDELINES.md` | Work-In-Progress limits and policies |
| `CONTRIBUTING.md` | Contributor setup guide and PR process |

> **Legacy docs** (pre-Magnetar) are preserved with the `_original` suffix.

---

## Progress Model Overview

Progress is tracked through milestones → tasks → state transitions:

```
planned → ready → in_progress → in_review → done
                       ↓
                   blocked (temporary)
```

- Every **state change** is recorded in `BITACORA.md`.
- Milestones aggregate task completion percentages.
- `STATUS.md` provides a real-time snapshot of overall health.

---

## YAML Project Schema

`projects/_template.project.yml` is the canonical machine-readable schema. It contains:

- **`metadata`** — Project name, description, start date.
- **`stakeholders`** — Key people and their roles.
- **`milestones`** — IDs, names, and target dates.
- **`tasks`** — IDs, titles, owners, effort, and current state.
- **`risks`** — Registry of potential risks and mitigations.
- **`reporting`** — Hooks for automated reports.

The YAML file is the authoritative reference that AI agents and CI pipelines must parse.

---

## Guidance for AI Collaborators

AI agents working on this project **must**:

1. **Parse** `projects/etorohelper.project.yml` before taking any action.
2. **Use** `PLAN.md` and `STATUS.md` to determine current focus and open tasks.
3. **Respect** `RULES.md`, `WIP_GUIDELINES.md`, and `BRANCHING_MODEL.md` at all times.
4. **Update** `BITACORA.md` after completing any unit of work, documenting assumptions when uncertain.
5. **Not open PRs** unless the task state is `in_review`.

---

## Architecture Diagram (Overview)

```
┌─────────────────────────────────────┐
│        Governance Standards         │
│  RULES.md · BRANCHING_MODEL.md      │
│  WIP_GUIDELINES.md · CONTRIBUTING.md│
└────────────────┬────────────────────┘
                 │ informs
                 ▼
┌─────────────────────────────────────┐
│             Planning                │
│   PLAN.md · STATUS.md · BITACORA.md │
│   projects/etorohelper.project.yml  │
└────────────────┬────────────────────┘
                 │ drives
                 ▼
┌─────────────────────────────────────┐
│         Execution Artifacts         │
│  src/ · tests/ · main.py            │
│  REQUIREMENTS.md · ARCHITECTURE.md  │
│  TESTING.md · BLOCKERS.md           │
└────────────────┬────────────────────┘
                 │ demonstrated by
                 ▼
┌─────────────────────────────────────┐
│              Examples               │
│   example/ · 2025-12-15/ output     │
└─────────────────────────────────────┘
```

---

## Applying This Template

1. **Copy** this repository structure to a new project folder.
2. **Replace** all placeholder content (project name, dates, usernames) with project-specific details.
3. **Instantiate and validate** a project YAML file from `projects/_template.project.yml`.
4. **Establish initial milestones** and log the initial state in `PLAN.md`, `STATUS.md`, and `BITACORA.md`.

---

## Validating Canon Compliance

Use this checklist to confirm that the project follows the Magnetar canon:

- [ ] All required files exist: `README.md`, `PLAN.md`, `BITACORA.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, `RULES.md`, `STATUS.md`, `TESTING.md`, `BLOCKERS.md`, `BRANCHING_MODEL.md`, `WIP_GUIDELINES.md`, `CONTRIBUTING.md`.
- [ ] `projects/etorohelper.project.yml` exists and matches the schema in `projects/_template.project.yml`.
- [ ] `BITACORA.md` is updated chronologically (most recent entry first).
- [ ] Active branches follow the naming rules in `BRANCHING_MODEL.md`.
- [ ] Testing commitments match the strategy defined in `TESTING.md`.
- [ ] All active blockers are documented in `BLOCKERS.md` with owner and severity.

---

*Original pre-Magnetar README preserved as `README_original.md`.*
