### Extracted Information

Here’s the structured data extracted from the HTML, including **performance metrics**, **asset allocation**, **dividends**, **trading statistics**, and **ESG ratings**:

---

## **Table Summary**

| **Category**               | **Metric**                         | **Value**                     |
|----------------------------|------------------------------------|-------------------------------|
| **Performance**            | Copiers (12M)                      | 0                             |
| **Performance**            | User Return vs. SPX500             | User: **+15.91%**, SPX500: **+13.61%** |
| **Asset Allocation**      | Copy & SmartPortfolios             | 57.6%                         |
| **Asset Allocation**      | Stocks                             | 37.4%                         |
| **Asset Allocation**      | Crypto                             | 2.9%                          |
| **Asset Allocation**      | ETF                                | 2.2%                          |
| **Dividends**              | Dividend Yield                     | 1.40%                         |
| **Dividends**              | Assets Paying Dividends           | 34                            |
| **Dividends**              | Annual Income                      | $182.96                       |
| **Dividends**              | Monthly Income                     | $15.25                        |
| **Dividends**              | Daily Income                       | $0.50                         |
| **Dividends**              | Income (Last 12 Months)           | $360.08                       |
| **Trading Statistics**    | Total Trades (12M)                 | 653                           |
| **Trading Statistics**    | Avg. Profit per Trade              | +31.63%                       |
| **Trading Statistics**    | Avg. Loss per Trade                | -22.11%                       |
| **Trading Statistics**    | Profitable Trades                  | 46.25%                        |
| **Additional Stats**      | Trades per Week                    | 141.71                        |
| **Additional Stats**      | Avg. Holding Time                  | 14.5 months                   |
| **Additional Stats**      | Account Active Since               | 4/15/21                       |
| **Additional Stats**      | Profitable Weeks                   | 65.45%                        |
| **ESG Rating**            | Overall ESG Score                  | 54 (Medium)                   |
| **ESG Rating**            | Environmental                      | 54                            |
| **ESG Rating**            | Social                             | 53                            |
| **ESG Rating**            | Governance                         | 55                            |
| **ESG Flags**             | Fossil Fuels                       | 2%                            |
| **ESG Flags**             | Tobacco                            | 2%                            |
| **ESG Flags**             | Thermal Coal                       | 1%                            |

---

## **JSON Output**

```json
{
  "performance": {
    "copiers_12m": 0,
    "user_vs_spx500": {
      "user": "+15.91%",
      "spx500": "+13.61%"
    }
  },
  "asset_allocation": {
    "copy_and_smart_portfolios": "57.6%",
    "stocks": "37.4%",
    "crypto": "2.9%",
    "etf": "2.2%"
  },
  "dividends": {
    "dividend_yield": "1.40%",
    "assets paying dividends": 34,
    "annual_income": "$182.96",
    "monthly_income": "$15.25",
    "daily_income": "$0.50",
    "income_last_12m": "$360.08"
  },
  "trading_statistics": {
    "total_trades_12m": 653,
    "average_profit": "+31.63%",
    "average_loss": "-22.11%",
    "profitable_trades_percentage": "46.25%"
  },
  "additional_stats": {
    "trades_per_week": 141.71,
    "average_holding_time": "14.5 months",
    "account_active_since": "4/15/21",
    "profitable_weeks": "65.45%"
  },
  "esg_rating": {
    "overall_score": 54,
    "environmental": 54,
    "social": 53,
    "governance": 55,
    "involvement_flags": {
      "fossil_fuels": "2%",
      "tobacco": "2%",
      "thermal_coal": "1%"
    }
  }
}
```

---

## **Explanation of Extraction & Python Parsing**

### **What Was Extracted?**
1. **Performance Metrics**:  
   - Copiers over 12 months (`0`).  
   - User vs. market performance (`SPX500`).  

2. **Asset Allocation**:  
   - Percentage breakdown of assets (e.g., `Copy & SmartPortfolios: 57.6%`).  

3. **Dividends**:  
   - Yield, number of dividend-paying assets, and income amounts.  

4. **Trading Statistics**:  
   - Trade volume, profit/loss averages, and profitability.  

5. **ESG Data**:  
   - Overall ESG score (`54`) and subsystem scores (`Environmental: 54`, `Social: 53`, `Governance: 55`).  
   - Involvement flags (e.g., `Fossil Fuels: 2%`).  

---

### **How to Parse This in Python**

Use **BeautifulSoup** to extract data from HTML elements based on CSS classes/IDs. Below is a template:

```python
import requests
from bs4 import BeautifulSoup
import json
import re

# Fetch HTML content (replace URL with actual page)
url = "https://example.com/user-stats"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

# --- Example Extractors ---
def extract_number(text):
    """Extract numeric values (handles percentages, currencies, etc.)"""
    match = re.search(r"[\d.,]+%", text) or re.search(r"[\d.,]+", text)
    if match:
        return match.group().replace("%", "").replace("$", "").strip()
    return None

# 1. Asset Allocation (from bars)
allocation Bars = soup.select(".bar.asset-type-bar")
allocation = {}
for bar in allocation Bars:
    label = bar.select_one(".ets-info").text.strip()
    value = bar.select_one(".ets-bold-num").text.strip()
    allocation[label] = value

# 2. ESG Score
esg_score = soup.select_one(".score-value").text.strip()  # "54"

# 3. Dividend Yield
dividend_yield = soup.select_one(".ets-num-xxl.ets-bold-num").text.strip()  # "1.40%"

# 4. Trading Stats
trades = soup.select_one(".ets-num-l.ets-neutral-100").text.strip()  # "653"

# 5. Performance Comparison
user_return = soup.select_one('[automation-id="compare-user-performance-value"]').text.strip()  # "+15.91%"
market_return = soup.select_one('[automation-id="compare-market-performance-value"]').text.strip()  # "+13.61%"

# --- Build JSON ---
data = {
    "asset_allocation": allocation,
    "esg_score": esg_score,
    "dividend_yield": dividend_yield,
    "trading_volume": trades,
    "performance": {
        "user": user_return,
        "spx500": market_return
    }
}

print(json.dumps(data, indent=2))
```

---

### **Key Parsing Strategies**
1. **CSS Selectors**:  
   - Use classes like `.ets-bold-num` for percentages, `.ets-num-xl` for large numbers, and `[automation-id="..."]` for specific elements.  
   - Example: `soup.select_one('[automation-id="user-stats-esg-score-value"]')` targets the ESG score.  

2. **Regex Extraction**:  
   - Clean strings with `re.search()` to extract numbers (e.g., `re.search(r"[\d.]+%", text)`).  

3. **Handling Dynamic Content**:  
   - If data is loaded via JavaScript, use tools like **Selenium** or **Playwright** to render the page first.  

4. **Edge Cases**:  
   - Some values (e.g., `N/A` for copiers) need special handling.  

---

This approach ensures robust extraction of structured data from complex HTML dashboards.