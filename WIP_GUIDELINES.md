# WIP Guidelines for EtoroHelper
> Work-In-Progress (WIP) limits ensure focus, reduce context-switching, and keep the project flowing smoothly.
---
## 1. WIP Limits
| Participant | Max `in_progress` Tasks |
|-------------|------------------------|
| Individual contributor (human) | **2** |
| AI agent (single session) | **2** |
| Total project WIP | **4** (recommended) |
These limits apply to tasks in the `in_progress` state as tracked in `PLAN.md`.
---
## 2. Why WIP Limits Matter
- **Focus:** Limits prevent over-commitment and shallow work.
- **Flow:** Tasks move to `done` faster when fewer are in flight simultaneously.
- **Transparency:** The current WIP is always visible in `STATUS.md` and `PLAN.md`.
---
## 3. Requesting a WIP Exception
If a situation genuinely requires exceeding the WIP limit:
1. **Document the reason** in `BITACORA.md` — include the timestamp, justification, and which tasks are affected.
2. **Notify the project lead** (edward) or log it as a `Discovery` entry if working autonomously.
3. **Define a resolution timeframe** — the exception must be temporary (resolve within 1 day).
4. **Return to limit** — once the exception task is resolved or moved to `in_review`, immediately reduce WIP.
Exceptions are **not** a workaround for poor planning. Recurring exceptions must trigger a retrospective entry in `BITACORA.md`.
---
## 4. WIP and Blockers
- A task in `blocked` state **does not count** against the WIP limit.
- However, the blocker must be logged in `BLOCKERS.md` immediately.
- The contributor should pick up another `ready` task while the blocker is unresolved, staying within the WIP limit for `in_progress` tasks.
---
## 5. WIP Monitoring
- `STATUS.md` → *Active Tasks* section shows current in-flight work.
- `PLAN.md` → *Task Backlog* table reflects current state of all tasks.
- Review WIP at the start of every work session before claiming a new task.
