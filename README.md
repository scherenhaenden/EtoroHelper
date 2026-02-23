# EtoroHelper

EtoroHelper is a Python-based tool designed to extract, parse, and organize data from eToro, a popular social trading platform. It automates the process of downloading user profiles, portfolios, and statistics, and converts them into structured JSON and Markdown formats for easy analysis and reporting.

## Overview

The tool consists of two main functionalities:

1. **Local Portfolio Parsing**: Parses a locally stored HTML file containing portfolio data and generates JSON and Markdown outputs.
2. **User Data Download and Parsing**: Downloads HTML pages for a specific eToro user (trader or investor) and parses their performance and statistics data.

## Features

- **Automated Dependency Installation**: Automatically installs required Python packages if not present.
- **Headless Browser Scraping**: Uses Selenium with Chrome WebDriver to download dynamic web content from eToro.
- **Data Extraction**: Extracts detailed information including portfolio holdings, performance metrics, trading statistics, asset allocation, dividends, and ESG ratings.
- **Output Formats**: Generates both JSON (for programmatic use) and Markdown (for human-readable reports) files.
- **Error Handling**: Includes fallback mechanisms for partial data retrieval and debugging.

## Requirements

- Python 3.12 or higher
- Google Chrome browser installed
- Internet connection for downloading user data

## Dependencies

The following Python packages are automatically installed if missing:

- `beautifulsoup4` (bs4): For HTML parsing
- `requests`: For HTTP requests (though primarily used via Selenium)
- `selenium`: For browser automation
- `webdriver-manager`: For automatic ChromeDriver management

## Project Structure

```
EtoroHelper/
├── main.py                 # Main entry point script
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── src/
│   ├── __init__.py
│   ├── dependencies.py     # Dependency installation utilities
│   ├── downloader.py       # Selenium-based web scraping
│   ├── parser.py           # Portfolio data extraction
│   ├── performance_parser.py # User performance data extraction
│   └── stats_parser.py     # User statistics data extraction
├── docs/
│   ├── Requirements_Engineering.md
│   ├── Software_Specification.md
│   └── System_Architecture.md
├── example/                # Example input and output files
├── [date]/                 # Date-based run directories
    ├── input/              # Local input files
    ├── output/             # Generated output files
    └── portfolio/          # Optional username fallback file
└── downloads/
    └── [username]/[date]/  # Downloaded profile/stats/chart HTML + parsed outputs
```

## Installation

1. Clone or download the project files.
2. Ensure Python 3.12+ is installed.
3. Install dependencies (automatically handled by the script):
   ```bash
   python3 main.py
   ```

## Usage

### Command Line Options

The program supports the following command-line arguments:

- `--user USERNAME`: eToro username directly (e.g., `scherenhaenden`)
- `--user-url URL`: eToro user profile URL (e.g., `https://www.etoro.com/people/username`)
- `--base-dir DIR`: Base directory for input/output (default: current date in YYYY-MM-DD format)

### Examples

#### Download and analyze a specific user:
```bash
python3 main.py --user scherenhaenden
```

#### Use a user URL and custom base directory:
```bash
python3 main.py --user-url https://www.etoro.com/people/scherenhaenden --base-dir my-analysis
```

#### Traditional usage (backward compatible):
```bash
# Create directory structure and files manually
mkdir -p 2025-12-15/portfolio
echo "scherenhaenden" > 2025-12-15/portfolio/person.txt
python3 main.py --base-dir 2025-12-15
```

### Preparation

1. **For direct username usage**: Provide `--user`.

2. **For URL-based usage**: Provide `--user-url`; the program extracts the username automatically.

3. **For local portfolio parsing** (optional):
   - Place your eToro portfolio HTML file in `{base_dir}/input/InputContent.txt`.

4. **For traditional file-based usage**:
   - Create `{base_dir}/portfolio/person.txt` containing the eToro username.

### Running the Program

Execute the main script with appropriate arguments:

```bash
python3 main.py --user-url https://www.etoro.com/people/username
```

The script will:

1. Install missing dependencies.
2. Extract username from the provided URL (if using --user-url).
3. Parse the local portfolio file if present.
4. Download user data using Selenium.
5. Parse and generate outputs for performance and statistics.

### Output Structure

After running, outputs are split by source:

- `{base_dir}/output/portfolio.json` and `{base_dir}/output/portfolio.md`: Parsed local portfolio file (if present)
- `downloads/{username}/{yyyy-mm-dd}/`: User-specific download and parsing output
  - `profile.html`, `stats.html`, `portfolio.html`, `chart.html`
  - `performance.json` / `performance.md`
  - `stats.json` / `stats.md`

## Data Extraction Details

### Portfolio Parsing

Extracts from eToro portfolio overview tables:

- Ticker symbols and company names
- Asset types (Instruments or Persons/Copy Traders)
- Current prices, net values, P&L data
- Percentage changes and gains
- Market exposure information

### Performance Parsing

From user profile pages:

- Annual performance data (yearly gains/losses)
- YTD and 2-year returns
- Average risk rating (last 7 days)
- Profitable weeks percentage

### Statistics Parsing

From user stats pages:

- **Performance Metrics**:
  - Number of copiers (12 months)
  - User vs. S&P 500 returns

- **Asset Allocation**:
  - Breakdown by asset class (Stocks, Crypto, ETF, etc.)

- **Dividends**:
  - Dividend yield
  - Assets paying dividends
  - Income statistics (annual, monthly, daily, last 12 months)

- **Trading Statistics**:
  - Total trades (12 months)
  - Profitable trades percentage
  - Average profit/loss per trade

- **Additional Stats**:
  - Trades per week
  - Average holding time
  - Account active since date
  - Profitable weeks

- **ESG Rating**:
  - Overall ESG score
  - Sub-scores for Environmental, Social, Governance

## Configuration

`--base-dir` controls only local portfolio parsing input/output (`{base_dir}/input` and `{base_dir}/output`). User profile downloads always go to `downloads/{username}/{yyyy-mm-dd}/`.

## Troubleshooting

- **WebDriver Issues**: Ensure Google Chrome is installed and up-to-date.
- **Missing Data**: eToro may change their page structure; the parsers use automation IDs and CSS selectors that may need updates.
- **Partial Downloads**: Failed downloads save partial HTML with `_failed` suffix for debugging.

## Legal and Ethical Considerations

- This tool is for personal use only.
- Respect eToro's terms of service and robots.txt.
- Do not use for commercial purposes without permission.
- Rate limiting and respectful scraping practices are recommended.

## Contributing

To extend the tool:

1. Update parsers in `src/` for new data fields.
2. Add new output formats in generation functions.
3. Enhance error handling and logging.

## License

[Add license information here]
