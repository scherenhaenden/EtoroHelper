# Contributing to EtoroHelper
> EtoroHelper is a personal-use project. This guide is for contributors (and AI agents) who want to extend or fix the tool.
---
## 1. Development Environment Setup
### Prerequisites
- Python 3.12 or higher
- Google Chrome (stable channel)
- `uv` package manager — [install uv](https://docs.astral.sh/uv/getting-started/installation/)
### Setup Steps
```bash
# 1. Clone the repository
git clone <repo-url>
cd EtoroHelper
# 2. Install dependencies via uv
uv sync
# 3. Run the test suite to verify setup
uv run pytest -v
```
---
## 2. Project Structure
```
EtoroHelper/
├── main.py                    # Entry point
├── src/                       # Core modules
│   ├── url_utils.py
│   ├── downloader.py
│   ├── parser.py
│   ├── performance_parser.py
│   └── stats_parser.py
├── tests/                     # Test suite
│   ├── conftest.py
│   ├── test_url_utils.py
│   ├── test_downloader.py
│   └── test_main.py
├── projects/                  # Project YAML schema & instance
├── example/                   # Reference input/output
└── [Magnetar governance files]
```
---
## 3. Making Changes
### Workflow
1. **Read** `RULES.md`, `BRANCHING_MODEL.md`, and `WIP_GUIDELINES.md`.
2. **Check** `PLAN.md` for the relevant task and ensure its state is `ready` or `in_progress`.
3. **Create a branch** following the naming convention: `<type>/<description>`.
4. **Make your changes** — keep commits focused and atomic.
5. **Write or update tests** — maintain coverage above 80%.
6. **Update documentation** — update `REQUIREMENTS.md` or `ARCHITECTURE.md` if the change affects the system design.
7. **Update `BITACORA.md`** with a log entry describing your work.
8. **Open a Pull Request** — only when the task is in `in_review` state.
### Code Style
- Follow PEP 8 for Python code.
- Use type hints where practical.
- Prefer explicit `open(..., encoding='utf-8')` for all file operations.
- Keep functions small and single-purpose.
---
## 4. Submitting a Pull Request
Your PR description must include:
- **Task ID(s):** e.g., `Closes task-301`
- **Summary:** What changed and why.
- **Testing:** How you verified the change (test run output, manual steps).
- **Documentation:** Which docs were updated.
- **`BITACORA.md` entry:** Confirm you added a log entry.
### PR Title Format
```
[task-XXX] Short imperative description
```
Example: `[task-205] Fix test_downloader encoding issues`
---
## 5. Parser Updates
When eToro changes their page structure:
1. Identify the broken selector using browser DevTools on the eToro page.
2. Update the relevant parser in `src/`.
3. Add or update a test with a minimal HTML fixture covering the new selector.
4. Log the discovery in `BITACORA.md` under the `Discovery` category.
---
## 6. AI Agent Contributions
AI agents must follow all rules in `RULES.md` and additionally:
- Parse `projects/etorohelper.project.yml` before starting.
- Validate the current WIP count before claiming a task.
- Always update `BITACORA.md` after completing work.
- Do not delete existing files — rename with `_original` suffix if replacement is needed.
