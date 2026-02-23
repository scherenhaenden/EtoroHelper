# Requirements Engineering

## 1. Introduction

### 1.1 Purpose
This document outlines the requirements for the EtoroHelper system, a Python-based tool for extracting, parsing, and organizing data from the eToro social trading platform. The system automates data collection and processing to provide structured insights into portfolios and user performance metrics.

### 1.2 Scope
EtoroHelper covers:
- Automated installation of dependencies
- Parsing of local eToro portfolio HTML files
- Web scraping of eToro user profiles, statistics, and performance data
- Generation of JSON and Markdown output formats
- Error handling and fallback mechanisms

### 1.3 Definitions and Acronyms
- **eToro**: Social trading platform
- **HTML**: HyperText Markup Language
- **JSON**: JavaScript Object Notation
- **Markdown**: Lightweight markup language
- **Selenium**: Browser automation tool
- **WebDriver**: Interface for controlling web browsers
- **ESG**: Environmental, Social, and Governance

## 2. Overall Description

### 2.1 Product Perspective
EtoroHelper is a standalone Python application that interfaces with eToro's web platform through automated browser interactions and local file processing. It serves users who need to analyze eToro data without manual extraction.

### 2.2 Product Functions
- Install required Python packages automatically
- Parse portfolio data from HTML files
- Download user-specific web pages using headless browser
- Extract structured data from HTML content
- Generate multiple output formats
- Handle errors gracefully with partial data recovery

### 2.3 User Characteristics
- **Primary Users**: Individual investors and analysts interested in eToro data
- **Technical Proficiency**: Basic to intermediate Python knowledge
- **Usage Frequency**: Occasional to regular data extraction tasks

### 2.4 Constraints
- Requires Python 3.12+
- Depends on Google Chrome browser
- Subject to eToro's terms of service
- Limited by web page structure changes

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Dependency Management
**FR-1.1**: The system shall automatically detect and install missing Python packages.
- **FR-1.1.1**: Check for presence of beautifulsoup4, requests, selenium, webdriver-manager
- **FR-1.1.2**: Install packages using pip if not found
- **FR-1.1.3**: Bootstrap pip if necessary

#### 3.1.2 Local Portfolio Parsing
**FR-2.1**: The system shall parse eToro portfolio HTML files.
- **FR-2.1.1**: Read HTML content from specified input file
- **FR-2.1.2**: Extract portfolio table data including tickers, names, prices, P&L
- **FR-2.1.3**: Generate JSON output with structured portfolio data
- **FR-2.1.4**: Generate Markdown table output for human readability

#### 3.1.3 Web Data Download
**FR-3.1**: The system shall download eToro user pages using Selenium.
- **FR-3.1.1**: Configure headless Chrome WebDriver
- **FR-3.1.2**: Navigate to profile, stats, portfolio, and chart URLs
- **FR-3.1.3**: Wait for dynamic content to load using appropriate selectors
- **FR-3.1.4**: Save HTML content to local files
- **FR-3.1.5**: Handle download failures with partial content saving

#### 3.1.4 Performance Data Extraction
**FR-4.1**: The system shall extract performance metrics from profile pages.
- **FR-4.1.1**: Parse annual performance data from chart tooltips
- **FR-4.1.2**: Extract YTD and multi-year returns
- **FR-4.1.3**: Capture risk ratings and profitable weeks data
- **FR-4.1.4**: Generate JSON and Markdown performance reports

#### 3.1.5 Statistics Data Extraction
**FR-5.1**: The system shall extract comprehensive statistics from stats pages.
- **FR-5.1.1**: Parse performance metrics (copiers, user vs market returns)
- **FR-5.1.2**: Extract asset allocation breakdowns
- **FR-5.1.3**: Capture dividend information and income statistics
- **FR-5.1.4**: Extract trading statistics (total trades, profitability, avg P&L)
- **FR-5.1.5**: Parse additional stats (trades/week, holding time, account age)
- **FR-5.1.6**: Extract ESG ratings and sub-scores

#### 3.1.6 Output Generation
**FR-6.1**: The system shall generate multiple output formats.
- **FR-6.1.1**: Create JSON files with complete data structures
- **FR-6.1.2**: Generate Markdown tables for all data sections
- **FR-6.1.3**: Organize outputs in date-based directory structure
- **FR-6.1.4**: Include user-specific subdirectories for downloaded data

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance
**NFR-1.1**: Web page downloads shall complete within 60 seconds per page.
**NFR-1.2**: HTML parsing shall process files under 10MB within 30 seconds.
**NFR-1.3**: Output generation shall complete within 10 seconds for typical data sets.

#### 3.2.2 Reliability
**NFR-2.1**: System shall handle network failures gracefully.
**NFR-2.2**: Partial data extraction shall be possible even with parsing errors.
**NFR-2.3**: Failed downloads shall save available content for debugging.

#### 3.2.3 Usability
**NFR-3.1**: Command-line interface shall be simple with single command execution.
**NFR-3.2**: Output files shall be self-documenting with clear structure.
**NFR-3.3**: Error messages shall be informative and actionable.

#### 3.2.4 Security
**NFR-4.1**: No sensitive data shall be stored or transmitted.
**NFR-4.2**: Web scraping shall respect robots.txt and rate limits.
**NFR-4.3**: Local files shall be processed without external data leakage.

#### 3.2.5 Maintainability
**NFR-5.1**: Code shall be modular with clear separation of concerns.
**NFR-5.2**: HTML selectors shall be configurable for eToro changes.
**NFR-5.3**: Logging shall be implemented for debugging purposes.

#### 3.2.6 Portability
**NFR-6.1**: System shall run on Linux, macOS, and Windows.
**NFR-6.2**: Python 3.12+ compatibility shall be maintained.
**NFR-6.3**: Chrome browser dependency shall be handled automatically.

## 4. Interface Requirements

### 4.1 User Interfaces
- Command-line interface with no interactive prompts
- File-based input/output using directory structure
- Console output for progress and error reporting

### 4.2 Software Interfaces
- **BeautifulSoup4**: HTML parsing library
- **Selenium WebDriver**: Browser automation
- **ChromeDriver**: WebDriver implementation
- **WebDriver Manager**: Automatic driver management

### 4.3 Hardware Interfaces
- Local file system for input/output operations
- Network interface for web downloads

## 5. Data Requirements

### 5.1 Input Data
- HTML files containing eToro portfolio data
- Text files with eToro usernames
- Directory structure with date-based organization

### 5.2 Output Data
- JSON files with structured data objects
- Markdown files with formatted tables
- Raw HTML files for reference and debugging

### 5.3 Data Formats
- Portfolio data: Array of objects with ticker, name, type, financial metrics
- Performance data: Object with annual data array and metrics object
- Statistics data: Nested object with performance, allocation, dividends, trading, additional stats, ESG sections

## 6. Assumptions and Dependencies

### 6.1 Assumptions
- eToro web page structure remains relatively stable
- Google Chrome is available on the system
- Internet connection is available for web scraping
- Python environment supports pip installation

### 6.2 Dependencies
- External Python packages as listed
- Chrome browser for Selenium
- Stable internet connection
- eToro platform availability

## 7. Requirements Traceability

| Requirement ID | Description | Priority | Status |
|----------------|-------------|----------|--------|
| FR-1.1 | Dependency management | High | Implemented |
| FR-2.1 | Local portfolio parsing | High | Implemented |
| FR-3.1 | Web data download | High | Implemented |
| FR-4.1 | Performance extraction | High | Implemented |
| FR-5.1 | Statistics extraction | High | Implemented |
| FR-6.1 | Output generation | High | Implemented |
| NFR-1.1 | Performance timing | Medium | Verified |
| NFR-2.1 | Reliability | High | Implemented |
| NFR-3.1 | Usability | High | Implemented |
| NFR-4.1 | Security | High | Implemented |
| NFR-5.1 | Maintainability | Medium | Implemented |
| NFR-6.1 | Portability | Medium | Verified |

## 8. Appendices

### 8.1 Glossary
- **Automation ID**: HTML attribute used by eToro for element identification
- **Copy Trader**: eToro feature allowing users to follow other traders
- **P&L**: Profit and Loss
- **YTD**: Year To Date

### 8.2 References
- eToro Platform: https://www.etoro.com
- BeautifulSoup Documentation: https://www.crummy.com/software/BeautifulSoup/
- Selenium Documentation: https://www.selenium.dev/documentation/
