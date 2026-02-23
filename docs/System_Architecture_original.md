# System Architecture

## 1. Introduction

### 1.1 Purpose
This document describes the architecture of the EtoroHelper system, including its components, design patterns, data flows, and technical decisions.

### 1.2 Scope
The architecture covers the overall system design, component interactions, data processing pipelines, and deployment considerations.

### 1.3 Architectural Drivers
- **Modularity**: Clear separation of concerns for maintainability
- **Automation**: Minimal user interaction required
- **Robustness**: Graceful error handling and recovery
- **Extensibility**: Easy addition of new data sources and outputs

## 2. Architectural Overview

### 2.1 System Context
EtoroHelper operates as a standalone Python application that:
- Reads local files from the file system
- Interacts with the eToro web platform via automated browser
- Processes HTML content to extract structured data
- Generates multiple output formats for analysis

### 2.2 Architectural Style
The system follows a **Layered Architecture** with clear separation:
- **Presentation Layer**: Command-line interface and file outputs
- **Application Layer**: Business logic for data processing
- **Infrastructure Layer**: External dependencies and system interactions

### 2.3 Key Architectural Patterns
- **Pipeline Pattern**: Sequential processing of data through parsing stages
- **Template Method Pattern**: Consistent parsing and output generation
- **Factory Pattern**: Dynamic creation of parsers based on content type
- **Strategy Pattern**: Pluggable output format generators

## 3. Component Architecture

### 3.1 Component Diagram

```
[Main Module]
    ├── Dependencies Manager
    ├── Local Parser
    ├── Web Downloader
    │   ├── Selenium Driver
    │   └── Page Handlers
    ├── Data Parsers
    │   ├── Portfolio Parser
    │   ├── Performance Parser
    │   └── Stats Parser
    └── Output Generators
        ├── JSON Generator
        └── Markdown Generator
```

### 3.2 Component Descriptions

#### 3.2.1 Main Module (main.py)
**Responsibilities**:
- Orchestrate the entire execution flow
- Manage directory structures
- Coordinate between components
- Handle high-level error recovery

**Interfaces**:
- Calls all other modules
- Reads configuration from file paths
- Writes progress to console

#### 3.2.2 Dependencies Manager (dependencies.py)
**Responsibilities**:
- Check for required packages
- Install missing dependencies
- Handle installation failures gracefully

**Design Patterns**:
- Singleton-like behavior for package checking
- Command pattern for installation execution

#### 3.2.3 Web Downloader (downloader.py)
**Responsibilities**:
- Configure browser automation
- Navigate to eToro pages
- Wait for content loading
- Save HTML to files

**Key Design Decisions**:
- Headless browser for server deployment
- Page-specific wait strategies
- Fallback content saving on errors

#### 3.2.4 Data Parsers
**Common Interface**:
- `extract_data(html_content: str) -> dict`
- `generate_json(data: dict, path: str) -> None`
- `generate_markdown(data: dict, path: str) -> None`

**Portfolio Parser (parser.py)**:
- Extracts tabular portfolio data
- Handles different asset types
- Robust data type conversion

**Performance Parser (performance_parser.py)**:
- Processes chart data and metrics
- Handles time-series performance data
- Extracts key performance indicators

**Stats Parser (stats_parser.py)**:
- Comprehensive statistics extraction
- Multiple data sections handling
- Complex nested data structures

#### 3.2.5 Output Generators
**Responsibilities**:
- Format data for different outputs
- Handle data type formatting
- Generate human-readable reports

## 4. Data Architecture

### 4.1 Data Flow Diagram

```
Input Files ──► Local Parser ──► Portfolio Data ──► Output Files
                    │
                    ▼
Web Scraping ──► HTML Files ──► Performance Parser ──► Performance Data
                    │
                    ▼
                    └─► Stats Parser ──► Statistics Data
```

### 4.2 Data Structures

#### 4.2.1 Portfolio Data
```python
TypedDict('PortfolioItem', {
    'ticker': Optional[str],
    'company_name': Optional[str],
    'type': Literal['Instrument', 'Person'],
    'price': Optional[float],
    'net_value': Optional[float],
    'asset_pnl': Optional[str],
    'change_percent': Optional[float],
    'daily_pnl': Optional[float],
    'gain_percent': Optional[float],
    'market_exposure': Optional[str]
})
```

#### 4.2.2 Performance Data
```python
TypedDict('PerformanceData', {
    'annualPerformance': List[Dict[str, str]],
    'additionalMetrics': Dict[str, str]
})
```

#### 4.2.3 Statistics Data
```python
TypedDict('StatsData', {
    'performance': Dict[str, Any],
    'asset_allocation': Dict[str, str],
    'dividends': Dict[str, str],
    'trading_statistics': Dict[str, str],
    'additional_stats': Dict[str, str],
    'esg_rating': Dict[str, str]
})
```

### 4.3 Data Processing Pipeline

1. **Input Validation**: Check file existence and format
2. **HTML Parsing**: Convert HTML to BeautifulSoup objects
3. **Element Selection**: Use CSS selectors and automation IDs
4. **Data Extraction**: Parse text content and attributes
5. **Type Conversion**: Convert strings to appropriate types
6. **Data Validation**: Ensure data consistency
7. **Output Formatting**: Generate JSON and Markdown

## 5. Interface Architecture

### 5.1 External Interfaces

#### 5.1.1 File System Interface
- **Input**: Read-only access to local files
- **Output**: Write access to generated files
- **Directory Structure**: Date-based organization

#### 5.1.2 Web Interface
- **Protocol**: HTTPS via Selenium WebDriver
- **Authentication**: None required (public eToro pages)
- **Rate Limiting**: Respectful delays between requests

#### 5.1.3 Browser Automation Interface
- **Driver**: Chrome WebDriver
- **Mode**: Headless for server environments
- **Capabilities**: JavaScript execution, dynamic content loading

### 5.2 Internal Interfaces

#### 5.2.1 Parser Interface
```python
class DataParser(ABC):
    @abstractmethod
    def extract_data(self, html_content: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def generate_json(self, data: Dict[str, Any], output_path: str) -> None:
        pass
    
    @abstractmethod
    def generate_markdown(self, data: Dict[str, Any], output_path: str) -> None:
        pass
```

#### 5.2.2 Downloader Interface
```python
class WebDownloader(ABC):
    @abstractmethod
    def download_person_data(self, person: str, download_dir: str) -> None:
        pass
    
    @abstractmethod
    def setup_driver(self) -> WebDriver:
        pass
```

## 6. Deployment Architecture

### 6.1 Execution Environment
- **Platform**: Cross-platform (Linux, macOS, Windows)
- **Runtime**: Python 3.12+
- **Dependencies**: Automatically managed
- **Browser**: Google Chrome (auto-managed)

### 6.2 Directory Structure
```
/project/
├── main.py
├── src/
│   ├── dependencies.py
│   ├── downloader.py
│   ├── parser.py
│   ├── performance_parser.py
│   └── stats_parser.py
├── docs/
├── [date]/
│   ├── input/
│   ├── output/
│   └── portfolio/
├── downloads/
│   └── [username]/[date]/
└── example/
```

### 6.3 Configuration Management
- **Version Control**: Git-based
- **Dependencies**: pyproject.toml and uv.lock
- **Code Configuration**: Hardcoded paths (configurable via constants)

## 7. Security Architecture

### 7.1 Threat Model
- **Data Exposure**: No sensitive data processed
- **Network Security**: HTTPS-only communications
- **Local Security**: File system access limited to project directories

### 7.2 Security Controls
- **Input Validation**: HTML content sanitization via BeautifulSoup
- **Error Handling**: No information leakage in error messages
- **Dependency Security**: Regular updates of packages

## 8. Performance Architecture

### 8.1 Performance Characteristics
- **Startup Time**: < 10 seconds (including dependency checks)
- **Processing Time**: < 60 seconds per user (web scraping + parsing)
- **Memory Usage**: < 500MB peak
- **Disk I/O**: Minimal, primarily output writing

### 8.2 Bottlenecks and Optimizations
- **Web Scraping**: Parallel page downloads (future enhancement)
- **HTML Parsing**: Efficient BeautifulSoup usage
- **Output Generation**: Streaming writes for large datasets

## 9. Maintainability Architecture

### 9.1 Code Organization
- **Modular Design**: Single responsibility principle
- **Separation of Concerns**: Parsing, downloading, output generation
- **DRY Principle**: Shared utilities and patterns

### 9.2 Extensibility Mechanisms
- **Plugin Architecture**: New parsers can be added
- **Configuration Files**: Selectors and URLs externalized
- **Template Methods**: Consistent processing patterns

### 9.3 Testing Architecture
- **Unit Tests**: Individual function testing
- **Integration Tests**: End-to-end workflow testing
- **Mock Objects**: Simulated web responses for testing

## 10. Evolution and Migration

### 10.1 Version Compatibility
- **Python Versions**: 3.12+ required
- **Package Versions**: Specified in pyproject.toml
- **Browser Compatibility**: Chrome latest stable

### 10.2 Migration Strategy
- **Data Formats**: Backward compatible JSON schemas
- **API Changes**: Versioned interfaces
- **Configuration**: Migration scripts for breaking changes

## 11. Quality Attributes

### 11.1 Reliability
- **Availability**: Single-run execution model
- **Fault Tolerance**: Graceful degradation on errors
- **Recoverability**: Partial results on failures

### 11.2 Usability
- **Learnability**: Simple command-line interface
- **Operability**: Automated execution
- **Accessibility**: Console-based, no GUI required

### 11.3 Efficiency
- **Time Behavior**: Fast execution for typical use cases
- **Resource Utilization**: Minimal system requirements
- **Scalability**: Linear scaling with data size

## 12. Risks and Mitigations

### 12.1 Technical Risks
- **eToro Changes**: Regular monitoring and selector updates
- **Browser Updates**: Automatic WebDriver management
- **Network Issues**: Retry mechanisms and offline fallbacks

### 12.2 Operational Risks
- **Dependency Conflicts**: Isolated environment recommendations
- **Large Datasets**: Memory monitoring and chunked processing
- **Rate Limiting**: Respectful scraping delays

## 13. Appendices

### 13.1 Component Interaction Diagrams
[Sequence diagrams would be included here]

### 13.2 Data Flow Diagrams
[Detailed data flow diagrams]

### 13.3 Deployment Diagrams
[Infrastructure deployment views]

### 13.4 Technology Stack
- **Language**: Python 3.12
- **Web Scraping**: Selenium WebDriver
- **HTML Parsing**: BeautifulSoup4
- **Browser**: Google Chrome
- **Package Management**: pip/uv
- **Version Control**: Git
