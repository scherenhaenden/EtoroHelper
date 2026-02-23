# Software Specification

## 1. Introduction

### 1.1 Purpose
This document provides detailed technical specifications for the EtoroHelper system, including system interfaces, data structures, algorithms, and implementation details.

### 1.2 Scope
The specification covers all components of the EtoroHelper application, from dependency management to output generation, with detailed descriptions of functionality, interfaces, and data handling.

### 1.3 References
- Requirements Engineering Document
- System Architecture Document
- Python 3.12 Documentation
- Selenium WebDriver Documentation

## 2. System Overview

### 2.1 System Architecture
EtoroHelper follows a modular architecture with the following components:
- Main execution module (main.py)
- Dependency management module (dependencies.py)
- Web scraping module (downloader.py)
- Data parsing modules (parser.py, performance_parser.py, stats_parser.py)
- Output generation utilities (integrated in parsers)

### 2.2 Execution Flow
1. Dependency installation and verification
2. Local portfolio file parsing (if present)
3. User data download via Selenium
4. Performance and statistics parsing
5. Output file generation

## 3. Module Specifications

### 3.1 Dependencies Module (dependencies.py)

#### 3.1.1 Purpose
Manages automatic installation of required Python packages.

#### 3.1.2 Functions

**install_if_not_exists(package, import_name=None)**
- **Parameters**:
  - `package`: str - Package name for pip installation
  - `import_name`: str, optional - Import name if different from package name
- **Returns**: None
- **Behavior**: Attempts to import the package; installs via pip if not found
- **Error Handling**: Falls back to pip bootstrapping if installation fails

**install_dependencies()**
- **Parameters**: None
- **Returns**: None
- **Behavior**: Installs all required packages (bs4, requests, selenium, webdriver-manager)

#### 3.1.3 Dependencies
- importlib
- subprocess
- sys

### 3.2 Downloader Module (downloader.py)

#### 3.2.1 Purpose
Handles web scraping of eToro user pages using Selenium.

#### 3.2.2 Functions

**download_person_data(person, download_dir)**
- **Parameters**:
  - `person`: str - eToro username
  - `download_dir`: str - Destination directory (e.g., `downloads/<user>/<date>`)
- **Returns**: None
- **Behavior**:
  - Configures headless Chrome WebDriver
  - Downloads profile, stats, portfolio, chart pages
  - Saves HTML content to output directory
- **Error Handling**:
  - Validates that `person` and `download_dir` are non-empty
  - Saves partial content on page-level failures
  - Always closes the WebDriver

#### 3.2.3 WebDriver Configuration
- Headless mode enabled
- Window size: 1920x1080
- User agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
- Sandbox disabled
- Shared memory usage disabled

#### 3.2.4 Page-Specific Wait Conditions
- **Profile**: Wait for '[automation-id="user-stats-chart-container"]'
- **Stats**: Wait for 'et-card-content'
- **Portfolio**: Wait for 'et-portfolio-group-list'
- **Chart**: Wait for 'et-chart-container'

### 3.3 Parser Module (parser.py)

#### 3.3.1 Purpose
Extracts portfolio data from HTML content.

#### 3.3.2 Data Structures

**Portfolio Item Object**:
```json
{
  "ticker": "string",
  "company_name": "string",
  "type": "Instrument" | "Person",
  "price": number | null,
  "net_value": number | null,
  "asset_pnl": "string" | null,
  "change_percent": number | null,
  "daily_pnl": number | null,
  "gain_percent": number | null,
  "market_exposure": "string" | null
}
```

#### 3.3.3 Functions

**extract_portfolio_data(html_content)**
- **Parameters**:
  - `html_content`: str - Raw HTML string
- **Returns**: list[dict] - Array of portfolio item objects
- **Algorithm**:
  1. Parse HTML with BeautifulSoup
  2. Find all 'et-table-row' elements
  3. For each row, extract data from cells using automation IDs
  4. Convert string values to appropriate types (float for numbers)
  5. Return structured data array

**generate_json(portfolio, output_path)**
- **Parameters**:
  - `portfolio`: list[dict] - Portfolio data
  - `output_path`: str - Output file path
- **Returns**: None
- **Behavior**: Writes JSON with 2-space indentation, preserving Unicode

**generate_markdown(portfolio, output_path)**
- **Parameters**:
  - `portfolio`: list[dict] - Portfolio data
  - `output_path`: str - Output file path
- **Returns**: None
- **Algorithm**:
  1. Create headers from first item keys
  2. Generate Markdown table with separators
  3. Format values (percentages, currency, etc.)
  4. Write to file

### 3.4 Performance Parser Module (performance_parser.py)

#### 3.4.1 Purpose
Extracts performance metrics from eToro profile pages.

#### 3.4.2 Data Structures

**Performance Data Object**:
```json
{
  "annualPerformance": [
    {"year": "string", "gainLoss": "string"}
  ],
  "additionalMetrics": {
    "renditeYTD": "string",
    "rendite2Y": "string",
    "averageRiskRatingLast7Days": "string",
    "profitableWeeks": "string"
  }
}
```

#### 3.4.3 Functions

**extract_performance_data(html_content)**
- **Parameters**:
  - `html_content`: str - Raw HTML string
- **Returns**: dict - Performance data object
- **Algorithm**:
  1. Parse HTML with BeautifulSoup
  2. Extract annual performance from chart candles
  3. Find metric values using automation IDs
  4. Return structured data

**generate_performance_json(data, output_path)**
- **Parameters**:
  - `data`: dict - Performance data
  - `output_path`: str - Output file path
- **Returns**: None

**generate_performance_markdown(data, output_path)**
- **Parameters**:
  - `data`: dict - Performance data
  - `output_path`: str - Output file path
- **Returns**: None
- **Algorithm**: Creates tables for annual performance and additional metrics

### 3.5 Stats Parser Module (stats_parser.py)

#### 3.5.1 Purpose
Extracts comprehensive statistics from eToro stats pages.

#### 3.5.2 Data Structures

**Statistics Data Object**:
```json
{
  "performance": {
    "copiers_12m": "string",
    "user_vs_spx500": {
      "user": "string",
      "spx500": "string"
    }
  },
  "asset_allocation": {
    "Stocks": "string",
    "Crypto": "string",
    ...
  },
  "dividends": {
    "dividend_yield": "string",
    "assets_paying_dividends": "string",
    ...
  },
  "trading_statistics": {
    "total_trades_12m": "string",
    "profitable_trades_percentage": "string",
    ...
  },
  "additional_stats": {
    "trades_per_week": "string",
    ...
  },
  "esg_rating": {
    "overall_score": "string",
    "environmental": "string",
    ...
  }
}
```

#### 3.5.3 Functions

**extract_stats_data(html_content)**
- **Parameters**:
  - `html_content`: str - Raw HTML string
- **Returns**: dict - Statistics data object
- **Algorithm**:
  1. Parse HTML with BeautifulSoup
  2. Extract data from various sections using automation IDs and CSS selectors
  3. Use fallback strategies for dynamic content
  4. Return comprehensive data structure

**generate_stats_json(data, output_path)**
- **Parameters**:
  - `data`: dict - Statistics data
  - `output_path`: str - Output file path
- **Returns**: None

**generate_stats_markdown(data, output_path)**
- **Parameters**:
  - `data`: dict - Statistics data
  - `output_path`: str - Output file path
- **Returns**: None
- **Algorithm**: Creates sectioned Markdown with tables for each data category

## 4. Interface Specifications

### 4.1 Command-Line Interface
- **Entry Point**: `python main.py`
- **Arguments**:
  - `--user`: Direct username
  - `--user-url`: URL-based username extraction
  - `--base-dir`: Local input/output base directory (portfolio parsing only)
- **Output**: Console messages for progress and errors

### 4.2 File System Interface
- **Input Files**:
  - `{base_dir}/portfolio/person.txt`: Optional username fallback file
  - `{base_dir}/input/InputContent.txt`: Portfolio HTML file
- **Output Files**:
  - `{base_dir}/output/portfolio.json`: Portfolio data
  - `{base_dir}/output/portfolio.md`: Portfolio report
  - `downloads/{username}/{yyyy-mm-dd}/performance.json`: Performance data
  - `downloads/{username}/{yyyy-mm-dd}/performance.md`: Performance report
  - `downloads/{username}/{yyyy-mm-dd}/stats.json`: Statistics data
  - `downloads/{username}/{yyyy-mm-dd}/stats.md`: Statistics report
  - `downloads/{username}/{yyyy-mm-dd}/*.html`: Raw downloaded pages

### 4.3 External Interfaces
- **BeautifulSoup**: HTML parsing with 'html.parser'
- **Selenium WebDriver**: Chrome driver with custom options
- **WebDriver Manager**: Automatic ChromeDriver installation

## 5. Data Processing Specifications

### 5.1 HTML Parsing Strategy
- Primary: Automation ID attributes (`automation-id`)
- Secondary: CSS class selectors
- Fallback: Text content searching with regex
- Error Recovery: Partial data extraction

### 5.2 Data Type Conversion
- **Currency Strings**: Remove '$' and ',' then convert to float
- **Percentage Strings**: Remove '%' and ',' then convert to float
- **Null Handling**: Use None for missing numeric values
- **Unicode Support**: Preserve non-ASCII characters

### 5.3 Output Formatting
- **JSON**: 2-space indentation, no ASCII encoding
- **Markdown**: GitHub-flavored tables with proper alignment
- **Value Formatting**: Currency with '$', percentages with '%'

## 6. Error Handling and Recovery

### 6.1 Exception Types
- **ImportError**: Package not installed
- **subprocess.CalledProcessError**: Pip installation failure
- **WebDriverException**: Browser automation issues
- **FileNotFoundError**: Missing input files
- **ValueError**: Data conversion failures

### 6.2 Recovery Mechanisms
- **Dependency Installation**: Bootstrap pip if needed
- **Web Scraping**: Save partial HTML on failures
- **Parsing**: Continue with available data, use null values
- **File Operations**: Create directories as needed

## 7. Performance Specifications

### 7.1 Timing Requirements
- **Dependency Check**: < 5 seconds
- **File Parsing**: < 10 seconds for 10MB files
- **Web Download**: < 60 seconds per page
- **Output Generation**: < 5 seconds

### 7.2 Resource Usage
- **Memory**: < 500MB for typical operations
- **Disk Space**: < 50MB for outputs including HTML files
- **Network**: Minimal, only during web scraping

## 8. Testing Specifications

### 8.1 Unit Testing
- Test each parser function with sample HTML
- Verify data extraction accuracy
- Test error handling scenarios

### 8.2 Integration Testing
- End-to-end execution with real data
- Directory structure validation
- Output format verification

### 8.3 Performance Testing
- Timing measurements for each component
- Memory usage monitoring
- Large file handling validation

## 9. Maintenance and Evolution

### 9.1 Configuration Management
- HTML selectors stored in code
- Version control with Git
- Dependency versions in pyproject.toml

### 9.2 Extensibility
- Modular parser design allows new data fields
- Output format additions possible
- New page types can be added to downloader

### 9.3 Monitoring and Logging
- Console output for progress tracking
- Error messages with context
- Debug information for troubleshooting

## 10. Appendices

### 10.1 Sample Data Structures
See individual module sections for detailed JSON schemas.

### 10.2 HTML Selector Reference
- `automation-id="portfolio-overview-table-body-cell-market-name"`: Ticker
- `automation-id="portfolio-overview-table-body-cell-market-last-name"`: Company name
- `automation-id="price-price-cell-investing-mode"`: Price value
- And many more as documented in parser code

### 10.3 Algorithm Flowcharts
[Text-based flowcharts would be included here in a full specification document]
