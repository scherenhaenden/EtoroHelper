# Blockers for EtoroHelper

> All impediments hindering project progress must be logged here immediately upon discovery. Update status upon resolution.

---

## Active Blockers

*No active blockers as of 2026-02-23.*

---

## Blocker Registry

| ID | Description | Severity | Created | Owner | Status |
|----|-------------|---------|---------|-------|--------|
| `blocker-001` | Test file encoding errors in `tests/test_downloader.py` causing integration test failures | Low | 2026-01-31 | edward | `in_review` |

### `blocker-001` Detail

- **Description:** Integration tests in `tests/test_downloader.py` fail due to file encoding mismatches when creating temporary test fixtures.
- **Affected task:** `task-205`
- **Severity:** Low — does not block the core application; only test infrastructure.
- **Mitigation:** Normalise all test fixture files to UTF-8 encoding; use `open(..., encoding='utf-8')` explicitly.
- **Resolution criteria:** All tests in `test_downloader.py` pass with `uv run pytest`.
- **Status:** `in_review` — work started; awaiting merge.

---

## Resolved Blockers

*None yet.*

---

## Escalation Process

If a blocker is **not resolved within 1 business day**:

1. **Escalate** by updating the severity to at least `high` in this table.
2. **Log** an escalation entry in `BITACORA.md` with timestamp and rationale.
3. **Notify** the project lead (edward) directly.
4. **Re-assess** scope: if the blocker affects a milestone target date, update `PLAN.md` and `STATUS.md`.

For `critical` blockers (production-breaking):
- Immediate escalation — no 1-day grace period.
- Open a `hotfix/<blocker-id>` branch immediately.
- Update `STATUS.md` within the hour.
