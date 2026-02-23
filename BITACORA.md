# Logbook of EtoroHelper

> This document is the immutable chronological logbook of the EtoroHelper project. It records decisions, state changes, discoveries, and key events in **reverse chronological order** (most recent first).
>
> **Immutability notice:** Do not alter past entries. Corrections must be made by adding a new entry that clarifies or supersedes the previous one.

---

**Timestamp:** 2026-02-23 11:00 UTC  
**Author:** GitHub Copilot (AI Agent)  
**Entry:** `task-301` and `task-302` — Magnetar Canonical Project Model applied to EtoroHelper. Created the following new files: `README.md` (replaced, original preserved as `README_original.md`), `RULES.md`, `PLAN.md`, `BITACORA.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, `STATUS.md`, `TESTING.md`, `BLOCKERS.md`, `BRANCHING_MODEL.md`, `WIP_GUIDELINES.md`, `CONTRIBUTING.md`, `projects/_template.project.yml`, `projects/etorohelper.project.yml`. Existing docs preserved with `_original` suffix. No files deleted. State of `task-301` changed from `in_progress` to `in_review`.

---

**Timestamp:** 2026-02-23 10:00 UTC  
**Author:** GitHub Copilot (AI Agent)  
**Entry:** Decision — Adopted Magnetar Canonical Project Model as the governance standard for EtoroHelper. All required Magnetar files will be added without deleting existing content. Pre-existing documentation preserved with `_original` suffix per owner instruction.

---

**Timestamp:** 2026-01-31 00:00 UTC  
**Author:** edward  
**Entry:** `ms-02` (CLI Enhancement) complete. `task-201`, `task-202`, `task-203`, `task-204` transitioned to `done`. `task-205` (integration tests for downloader) moved to `in_review` — encoding issues in test files noted; requires follow-up in `ms-04`.

---

**Timestamp:** 2025-12-15 00:00 UTC  
**Author:** edward  
**Entry:** `ms-01` (Project Foundation) complete. All core parsers (`parser.py`, `performance_parser.py`, `stats_parser.py`) and the Selenium downloader (`downloader.py`) are functional. JSON and Markdown outputs verified with real eToro user `scherenhaenden`. Tasks `task-101` through `task-105` transitioned to `done`.

---

**Timestamp:** 2025-12-15 00:00 UTC  
**Author:** edward  
**Entry:** Project EtoroHelper initialised. Initial repository structure created. Objective: automate eToro data extraction and convert to structured JSON/Markdown outputs.
