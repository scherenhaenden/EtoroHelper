# Canonical Plan of EtoroHelper
> This plan captures the project's milestones, tasks, estimates, and status. Its structure must be kept intact and updated in sync with `projects/etorohelper.project.yml` and `BITACORA.md`.
---
## Milestones Overview
| Milestone ID | Name | Target Date | Description | Completion Criteria |
|-------------|------|------------|-------------|-------------------|
| `ms-01` | Project Foundation | 2025-12-15 | Core scraping pipeline: local portfolio parsing, Selenium downloader, performance & stats parsers, JSON/MD output | All parsers functional; JSON + MD outputs generated for a real eToro user |
| `ms-02` | CLI Enhancement | 2026-01-31 | Add `--user` and `--user-url` CLI args; dynamic download path `downloads/{user}/{date}/`; backward compatibility | All new args functional; test suite green; README updated |
| `ms-03` | Canonical Governance | 2026-02-23 | Apply Magnetar Canonical Project Model; create all required governance files | All required files present; YAML schema instantiated; BITACORA initialised |
| `ms-04` | Stability & Coverage | 2026-03-31 | Integration tests; ≥80% coverage; CI validation of canonical file presence | CI green; coverage ≥80%; no open `critical` blockers |
---
## Task Backlog
| Task ID | Milestone | Title | Owner | Effort (pts) | Weight (%) | State | Notes |
|---------|-----------|-------|-------|-------------|-----------|-------|-------|
| `task-101` | `ms-01` | Implement local portfolio HTML parser | edward | 5 | 10% | `done` | `src/parser.py` |
| `task-102` | `ms-01` | Implement Selenium downloader | edward | 8 | 16% | `done` | `src/downloader.py` |
| `task-103` | `ms-01` | Implement performance parser | edward | 5 | 10% | `done` | `src/performance_parser.py` |
| `task-104` | `ms-01` | Implement statistics parser | edward | 5 | 10% | `done` | `src/stats_parser.py` |
| `task-105` | `ms-01` | Wire parsers in `main.py` with basic CLI | edward | 3 | 6% | `done` | `main.py` |
| `task-201` | `ms-02` | Add `--user` CLI argument | edward | 2 | 4% | `done` | `main.py` + `argparse` |
| `task-202` | `ms-02` | Add `--user-url` CLI argument + URL extraction | edward | 3 | 6% | `done` | `src/url_utils.py` |
| `task-203` | `ms-02` | Dynamic download path `downloads/{user}/{date}/` | edward | 2 | 4% | `done` | `src/downloader.py` |
| `task-204` | `ms-02` | Unit tests for URL utilities | edward | 3 | 6% | `done` | `tests/test_url_utils.py` |
| `task-205` | `ms-02` | Integration tests for downloader (mocked) | edward | 3 | 6% | `in_review` | `tests/test_downloader.py` — encoding issues noted |
| `task-301` | `ms-03` | Apply Magnetar Canonical Project Model | edward | 5 | 10% | `in_progress` | This task |
| `task-302` | `ms-03` | Instantiate `projects/etorohelper.project.yml` | edward | 2 | 4% | `in_progress` | Derived from `_template.project.yml` |
| `task-401` | `ms-04` | Add CI workflow for canonical file validation | edward | 3 | 6% | `planned` | GitHub Actions |
| `task-402` | `ms-04` | Achieve ≥80% test coverage | edward | 5 | 10% | `planned` | Coverage report via pytest-cov |
---
## Effort Summary
| Category | Points |
|----------|--------|
| **Total effort** | 54 pts |
| **Completed** (`done`) | 36 pts |
| **In progress / In review** | 10 pts |
| **Remaining** (`planned`) | 8 pts |
---
## State Definitions
| State | Meaning |
|-------|---------|
| `planned` | Identified but not yet refined or ready to start |
| `ready` | Refined, scoped, and ready to be picked up |
| `in_progress` | Actively being worked on (counts against WIP limit) |
| `in_review` | Work complete; awaiting peer review or merge approval |
| `blocked` | Cannot proceed; a blocker is logged in `BLOCKERS.md` |
| `done` | Accepted, merged, and verified |
---
## Change Management
This document must be updated whenever tasks change state or scope. All changes must also be reflected in `projects/etorohelper.project.yml` and recorded in `BITACORA.md`.
