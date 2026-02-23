# Testing Strategy for EtoroHelper
---
## 1. Types of Tests
### Unit Tests
- **Scope:** Individual functions and modules in isolation.
- **Location:** `tests/test_url_utils.py`, `tests/test_main.py`
- **Tools:** `pytest`, `unittest.mock`
- **Coverage target:** ≥80% line coverage across `src/`
- **Current status:** 12 URL parsing tests passing ✅
### Integration Tests
- **Scope:** Interaction between `main.py`, `downloader.py`, and the filesystem. Selenium is mocked.
- **Location:** `tests/test_downloader.py`
- **Tools:** `pytest`, `unittest.mock.patch`
- **Current status:** `in_review` — encoding issues in test fixtures being resolved (see `task-205`)
### End-to-End Tests
- **Scope:** Full pipeline execution against a real eToro URL.
- **Approach:** Manual validation during milestone reviews; automated E2E not in current scope (requires network access).
- **Target milestone:** `ms-04`
---
## 2. Code Coverage
| Target | Threshold |
|--------|-----------|
| Overall line coverage (`src/`) | ≥ 80% |
| Critical modules (`url_utils`, `parser`, `performance_parser`, `stats_parser`) | ≥ 90% |
Run coverage locally:
```bash
uv run pytest --cov=src --cov-report=term-missing
```
Coverage report will be added to CI output in `ms-04`.
---
## 3. Test Configuration
- **Test runner:** `pytest` (see `pytest.ini`)
- **Test discovery:** `tests/` directory
- **Markers:** Standard pytest markers (`-v`, `-x`, `--tb=short`)
- **Helper script:** `run_tests.py`
Run all tests:
```bash
uv run pytest
```
---
## 4. Mocking Strategy
| Component | Mocking Approach |
|-----------|----------------|
| Selenium WebDriver | `unittest.mock.patch('src.downloader.webdriver.Chrome')` |
| File system | `tempfile.TemporaryDirectory` in fixtures |
| `argparse` args | `unittest.mock.MagicMock` with explicit attribute assignment |
---
## 5. Bug Reporting Process
1. **Identify** the failing test or unexpected behaviour.
2. **Create a blocker** entry in `BLOCKERS.md` if it blocks a task.
3. **Log** the discovery in `BITACORA.md` under the `Discovery` category.
4. **Create a task** in `PLAN.md` (or annotate an existing task) with state `in_progress`.
5. **Fix** in a `fix/<description>` branch.
6. **Add a regression test** covering the exact failure scenario.
7. **Update** `BITACORA.md` upon resolution.
---
## 6. Known Issues
| Issue | Task | Status |
|-------|------|--------|
| Test file encoding errors in `test_downloader.py` | `task-205` | `in_review` |
---
## 7. CI Integration (Target: `ms-04`)
- GitHub Actions workflow will run `pytest` on every PR to `master`.
- Workflow will also validate presence of all required Magnetar canonical files.
- Coverage report will be uploaded as a workflow artifact.
