import json
import os
import sys

# Add the project root to sys.path to allow importing src.dependencies if run directly or from subfolder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dependencies import install_if_not_exists

# Check and install BeautifulSoup
install_if_not_exists("beautifulsoup4", "bs4")

from bs4 import BeautifulSoup

def extract_portfolio_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('div', class_='et-table-row')
    portfolio = []

    for row in rows:
        # 1. Extract Name/Ticker from the first cell
        first_cell = row.find('div', class_='et-table-first-cell')
        if not first_cell:
            continue
            
        ticker = None
        company_name = None
        item_type = "Instrument" # Default to Instrument
        
        # Ticker
        ticker_div = first_cell.find('div', attrs={'automation-id': 'portfolio-overview-table-body-cell-market-name'})
        if ticker_div:
            # Use the first span if available to avoid getting extra tags like "24/5"
            span = ticker_div.find('span')
            if span:
                ticker = span.text.strip()
            else:
                ticker = ticker_div.text.strip()
        
        # Company Name & Type Detection
        # Check for standard company name (Instrument)
        name_span = first_cell.find('span', attrs={'automation-id': 'portfolio-overview-table-body-cell-market-last-name'})
        if name_span:
            company_name = name_span.text.strip()
        else:
            # Check for mirror display name (Person/Copy Trader)
            mirror_span = first_cell.find('span', attrs={'automation-id': 'portfolio-overview-table-body-cell-market-mirror-display-name'})
            if mirror_span:
                company_name = mirror_span.text.strip()
                item_type = "Person"

        # 2. Extract Data Cells
        body_slot = row.find('div', class_='et-table-body-slot')
        if not body_slot:
            continue
            
        cells = body_slot.find_all('div', class_='et-table-cell', recursive=False)
        
        # Initialize fields in the desired order
        fields = {
            'ticker': ticker,
            'company_name': company_name,
            'type': item_type,
            'price': None,
            'net_value': None,
            'asset_pnl': None,
            'change_percent': None,
            'daily_pnl': None,
            'gain_percent': None,
            'market_exposure': None
        }
        
        # We expect at least 8 cells based on the table structure
        if len(cells) >= 8:
            # Cell 0: Price
            price_div = cells[0].find('div', attrs={'automation-id': 'price-price-cell-investing-mode'})
            if price_div:
                try:
                    fields['price'] = float(price_div.text.strip().replace(',', ''))
                except ValueError:
                    pass
            
            # Cell 2: Net Value (Equity)
            equity_span = cells[2].find('span', attrs={'automation-id': 'portfolio-overview-table-body-cell-equity'})
            if equity_span:
                try:
                    fields['net_value'] = float(equity_span.text.strip().replace('$', '').replace(',', ''))
                except ValueError:
                    pass

            # Cell 3: Asset P/L
            pnl_span = cells[3].find('span', attrs={'automation-id': 'portfolio-overview-table-body-cell-asset-pnl'})
            if pnl_span:
                fields['asset_pnl'] = pnl_span.text.strip()

            # Cell 4: Change %
            change_div = cells[4].find('div', attrs={'automation-id': 'portfolio-overview-table-body-cell-change'})
            if change_div:
                try:
                    fields['change_percent'] = float(change_div.text.strip().replace('%', '').replace(',', ''))
                except ValueError:
                    pass

            # Cell 5: Daily P/L
            daily_span = cells[5].find('span', attrs={'automation-id': 'portfolio-overview-table-body-cell-profit-amount-daily'})
            if daily_span:
                try:
                    fields['daily_pnl'] = float(daily_span.text.strip().replace('$', '').replace(',', ''))
                except ValueError:
                    pass

            # Cell 6: Gain %
            gain_span = cells[6].find('span', attrs={'automation-id': 'portfolio-overview-table-body-cell-gain'})
            if gain_span:
                try:
                    fields['gain_percent'] = float(gain_span.text.strip().replace('%', '').replace(',', ''))
                except ValueError:
                    pass

            # Cell 7: Market Exposure
            # This usually lacks a specific automation-id for the value, so we look for the body class
            exposure_span = cells[7].find('span', class_='table-cell-body')
            if exposure_span:
                fields['market_exposure'] = exposure_span.text.strip()
        
        portfolio.append(fields)

    return portfolio

def generate_json(portfolio, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(portfolio, f, indent=2, ensure_ascii=False)

def generate_markdown(portfolio, output_path):
    if not portfolio:
        return

    # Use the keys from the first item to determine headers and order
    headers = list(portfolio[0].keys())
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Generate Header Row
        header_names = [key.replace('_', ' ').title() for key in headers]
        f.write("| " + " | ".join(header_names) + " |\n")
        
        # Generate Separator Row
        f.write("| " + " | ".join(['-' * len(name) for name in header_names]) + " |\n")
        
        # Generate Data Rows
        for item in portfolio:
            row_values = []
            for key in headers:
                value = item.get(key)
                if value is None:
                    row_values.append("—")
                    continue
                
                # Apply formatting based on key name heuristics
                if isinstance(value, (int, float)):
                    if 'percent' in key or 'gain' in key or 'change' in key:
                        row_values.append(f"{value}%")
                    elif 'net_value' in key or 'daily_pnl' in key:
                        row_values.append(f"${value}")
                    elif 'price' in key:
                        row_values.append(f"${value}")
                    else:
                        row_values.append(str(value))
                else:
                    row_values.append(str(value))
            
            f.write("| " + " | ".join(row_values) + " |\n")
