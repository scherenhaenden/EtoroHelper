# Architecture of EtoroHelper

> This document supersedes `docs/System_Architecture_original.md` with the Magnetar canonical format. The original is preserved for reference.

---

## 1. High-Level Architecture Diagram

```
+------------------------------------------------------------------+
|                          main.py (CLI)                           |
|              argparse: --user / --user-url / --base-dir          |
+------------------------------------------+-----------------------+
                          |                  |
                          v                  v
+-------------------+  +------------------------------------------+
|  Local Portfolio  |  |         Web Download Pipeline            |
|  Parsing          |  |                                          |
|  (input HTML)     |  |  src/downloader.py (Selenium + Chrome)   |
|  src/parser.py    |  |  -> downloads/{user}/{date}/             |
+--------+----------+  |      profile.html                        |
         |             |      stats.html                          |
         v             |      portfolio.html                      |
 {base_dir}/output/    |      chart.html                          |
 portfolio.json        +------------------+-----------------------+
 portfolio.md                             |
                           +--------------+--------------+
                           v                             v
               +----------------------+    +---------------------+
               | performance_parser   |    |   stats_parser.py   |
               | .py                  |    |                     |
               +----------+-----------+    +----------+----------+
                          |                           |
                          v                           v
                 performance.json               stats.json
                 performance.md                stats.md
```

---

## 2. Component Descriptions

### `main.py` — Entry Point & Orchestrator
- **Responsibility:** Parses CLI arguments, resolves the username (from `--user`, `--user-url`, or `person.txt` fallback), triggers local portfolio parsing if input file exists, and invokes the download pipeline.
- **Technologies:** Python 3.12+, `argparse`, `os`, `datetime`.

### `src/url_utils.py` — URL Utility
- **Responsibility:** Validates and extracts usernames from eToro profile URLs. Validates bare usernames against `^[a-zA-Z0-9_-]+$`.
- **Technologies:** Python `re`.

### `src/dependencies.py` — Dependency Manager
- **Responsibility:** Automatically installs required pip packages (`beautifulsoup4`, `selenium`, `webdriver-manager`) if not already available.
- **Technologies:** `subprocess`, `importlib`.

### `src/downloader.py` — Web Scraper
- **Responsibility:** Launches a headless Chrome browser, navigates to eToro user pages (profile, stats, portfolio, chart), waits for Angular content to render, and saves the resulting HTML to `downloads/{username}/{date}/`.
- **Technologies:** `selenium`, `webdriver-manager`, `os`.

### `src/parser.py` — Portfolio Parser
- **Responsibility:** Parses a local eToro portfolio HTML file and extracts ticker symbols, company names, asset types, prices, P&L, and exposure data.
- **Technologies:** `beautifulsoup4`.

### `src/performance_parser.py` — Performance Parser
- **Responsibility:** Extracts annual performance data, YTD returns, risk rating, and profitable weeks percentage from a downloaded profile HTML.
- **Technologies:** `beautifulsoup4`.

### `src/stats_parser.py` — Statistics Parser
- **Responsibility:** Extracts copiers count, S&P 500 comparison, asset allocation, dividend data, trading statistics, and ESG scores from downloaded stats HTML.
- **Technologies:** `beautifulsoup4`.

---

## 3. Data Flow

```
CLI Input
    |
    +-- username resolved
    |
    +-- [optional] local portfolio HTML --> parser.py --> portfolio.{json,md}
    |
    +-- downloader.py
           | profile.html --> performance_parser.py --> performance.{json,md}
           | stats.html   --> stats_parser.py        --> stats.{json,md}
           | portfolio.html (saved for reference)
           +-- chart.html  (saved for reference)
```

---

## 4. Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Selenium over requests** | eToro pages are Angular-rendered (SPA); raw HTTP requests return empty shells. |
| **Headless Chrome** | Available on Linux CI/CD; matches the browser eToro targets. |
| **File-based output** | Keeps the tool stateless and reproducible without a database dependency. |
| **Date-stamped directories** | `downloads/{user}/{yyyy-mm-dd}/` makes runs comparable and avoids overwrites. |
| **BeautifulSoup4 for parsing** | Declarative, readable selectors; easy to update when eToro changes their DOM. |
| **Auto-dependency install** | Reduces setup friction; acceptable for a personal-use CLI tool. |

---

## 5. Deployment & Environment

- **OS:** Linux (primary), macOS (compatible)
- **Runtime:** Python 3.12+
- **Browser:** Google Chrome (stable channel)
- **Package Manager:** `uv` (see `pyproject.toml` and `uv.lock`)
- **Test Runner:** `pytest` (see `pytest.ini`)

---

*Original architecture preserved as `docs/System_Architecture_original.md`.*
