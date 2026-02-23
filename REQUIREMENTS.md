# Requirements for EtoroHelper

> This document supersedes `docs/Requirements_Engineering_original.md` with the Magnetar canonical format. The original is preserved for reference.

---

## 1. Functional Requirements

### Must-Have

| ID | Requirement |
|----|------------|
| `FR-01` | The system **must** accept an eToro username via `--user` CLI argument and download the user's profile, portfolio, statistics, and chart pages. |
| `FR-02` | The system **must** accept an eToro profile URL via `--user-url` CLI argument, extract the username, and proceed as FR-01. |
| `FR-03` | The system **must** parse a locally stored eToro portfolio HTML file (`{base_dir}/input/InputContent.txt`) and produce JSON and Markdown outputs. |
| `FR-04` | The system **must** extract performance data (annual returns, YTD, risk rating, profitable weeks) from the downloaded profile page. |
| `FR-05` | The system **must** extract statistics data (copiers, asset allocation, dividends, trading stats, ESG scores) from the downloaded stats page. |
| `FR-06` | The system **must** write all outputs to `downloads/{username}/{yyyy-mm-dd}/` for user-specific data. |
| `FR-07` | The system **must** install required Python dependencies automatically if they are missing. |
| `FR-08` | The system **must** handle partial download failures gracefully, saving partial HTML with a `_failed` suffix for debugging. |

### Should-Have

| ID | Requirement |
|----|------------|
| `FR-09` | The system **should** support a `--base-dir` argument to override the default date-based directory for local portfolio parsing. |
| `FR-10` | The system **should** read a username from `{base_dir}/portfolio/person.txt` as a fallback when no CLI argument is provided. |
| `FR-11` | The system **should** read a username from `{base_dir}/portfolio/person.txt` containing a URL as a fallback. |

### Could-Have

| ID | Requirement |
|----|------------|
| `FR-12` | The system **could** support CSV export as an additional output format. |
| `FR-13` | The system **could** support batch processing of multiple usernames from a list file. |

### Won't-Have (in current scope)

| ID | Requirement |
|----|------------|
| `FR-14` | The system **will not** implement a graphical user interface. |
| `FR-15` | The system **will not** store historical data in a database (file-based output only). |

---

## 2. Non-Functional Requirements

### Must-Have

| ID | Requirement |
|----|------------|
| `NFR-01` | The system **must** run on Python 3.12 or higher. |
| `NFR-02` | The system **must** use headless Chrome (via Selenium) to render Angular-based eToro pages. |
| `NFR-03` | The system **must** be executable with a single command: `python3 main.py --user <username>`. |
| `NFR-04` | The test suite **must** achieve >=80% code coverage (target for ms-04). |
| `NFR-05` | The system **must** not store user credentials or eToro session tokens on disk. |

### Should-Have

| ID | Requirement |
|----|------------|
| `NFR-06` | The system **should** complete a full user data download in under 120 seconds under normal network conditions. |
| `NFR-07` | The system **should** log meaningful error messages to stdout for all failure scenarios. |

### Could-Have

| ID | Requirement |
|----|------------|
| `NFR-08` | The system **could** support configurable wait timeouts for Selenium page loads. |

---

## 3. Constraints

- Requires Google Chrome browser installed on the host machine.
- Subject to eToro's Terms of Service; for personal use only.
- Page structure changes on eToro may require parser updates.

---

*Original requirements preserved as `docs/Requirements_Engineering_original.md`.*
