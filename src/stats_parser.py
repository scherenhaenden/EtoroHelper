import json
import re
from bs4 import BeautifulSoup

def extract_stats_data(html_content):
    """
    Parses the HTML of an eToro user's stats page to extract detailed statistics.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}

    # --- 1. Performance Metrics ---
    performance = {}
    
    # Copiers
    # Try multiple possible selectors
    copiers_elem = soup.find('div', attrs={'automation-id': 'stats-copiers-chart-copiers-value'})
    if not copiers_elem:
        copiers_elem = soup.find('span', attrs={'automation-id': 'copiers-value'})
    
    if copiers_elem:
        performance['copiers_12m'] = copiers_elem.text.strip()

    # User vs Market Return
    user_return_elem = soup.find('span', attrs={'automation-id': 'compare-user-performance-value'})
    market_return_elem = soup.find('span', attrs={'automation-id': 'compare-market-performance-value'})
    
    if user_return_elem or market_return_elem:
        performance['user_vs_spx500'] = {
            'user': user_return_elem.text.strip() if user_return_elem else None,
            'spx500': market_return_elem.text.strip() if market_return_elem else None
        }
    
    data['performance'] = performance

    # --- 2. Asset Allocation ---
    asset_allocation = {}
    # Look for the allocation container
    allocation_container = soup.find('div', attrs={'automation-id': 'stats-portfolio-allocation-container'})
    
    if allocation_container:
        # Try to find bars or list items within the container
        # Strategy 1: Look for specific automation-ids for names and values
        names = allocation_container.find_all('span', class_='name')
        values = allocation_container.find_all('span', class_='value')
        
        if len(names) == len(values) and names:
            for n, v in zip(names, values):
                asset_allocation[n.text.strip()] = v.text.strip()
        else:
            # Strategy 2: Iterate through rows/bars
            bars = allocation_container.find_all('div', class_=lambda x: x and 'bar' in x)
            for bar in bars:
                name = bar.find('span', class_='name')
                value = bar.find('span', class_='value')
                if name and value:
                    asset_allocation[name.text.strip()] = value.text.strip()

    # Fallback: Search entire soup for allocation-like structures if container not found
    if not asset_allocation:
        # Look for elements that might be allocation labels
        potential_labels = ['Stocks', 'Crypto', 'ETF', 'Indices', 'Commodities', 'Currencies', 'Copy & SmartPortfolios']
        for label in potential_labels:
            label_elem = soup.find(string=lambda x: x and label in x)
            if label_elem:
                # Try to find a nearby percentage value
                parent = label_elem.find_parent('div')
                if parent:
                    val = parent.find(string=re.compile(r'\d+\.?\d*%'))
                    if val:
                        asset_allocation[label] = val.strip()

    data['asset_allocation'] = asset_allocation

    # --- 3. Dividends ---
    dividends = {}
    div_yield_elem = soup.find('div', attrs={'automation-id': 'stats-dividends-yield-value'})
    if div_yield_elem:
        dividends['dividend_yield'] = div_yield_elem.text.strip()
    
    # Helper to find values by label text
    def find_value_by_label(label_text):
        # Find the label text
        label = soup.find(string=lambda x: x and label_text.lower() in x.lower())
        if label:
            # The value is often in a sibling element or a child of the parent
            # Traverse up to a container row/card and look for a value class
            parent = label.find_parent('div') # Immediate parent
            if parent:
                # Check siblings
                value = parent.find_next_sibling('div')
                if value and (value.get('class') == ['value'] or 'ets-num' in (value.get('class') or [])):
                    return value.text.strip()
                
                # Check children of parent's parent (common in grid layouts)
                grandparent = parent.parent
                if grandparent:
                    value = grandparent.find('span', class_='value') or grandparent.find('div', class_='value')
                    if value:
                        return value.text.strip()
        return None

    dividends['assets_paying_dividends'] = find_value_by_label('Assets Paying Dividends')
    dividends['annual_income'] = find_value_by_label('Annual Income')
    dividends['monthly_income'] = find_value_by_label('Monthly Income')
    dividends['daily_income'] = find_value_by_label('Daily Income')
    dividends['income_last_12m'] = find_value_by_label('Income (Last 12 Months)')

    data['dividends'] = dividends

    # --- 4. Trading Statistics ---
    trading_stats = {}
    total_trades_elem = soup.find('div', attrs={'automation-id': 'stats-trading-total-trades-value'})
    if total_trades_elem:
        trading_stats['total_trades_12m'] = total_trades_elem.text.strip()
    
    profitability_elem = soup.find('div', attrs={'automation-id': 'stats-trading-profitability-value'})
    if profitability_elem:
        trading_stats['profitable_trades_percentage'] = profitability_elem.text.strip()
        
    # Avg Profit/Loss
    avg_profit_elem = soup.find('div', attrs={'automation-id': 'stats-trading-avg-profit-value'})
    if avg_profit_elem:
        trading_stats['average_profit'] = avg_profit_elem.text.strip()
        
    avg_loss_elem = soup.find('div', attrs={'automation-id': 'stats-trading-avg-loss-value'})
    if avg_loss_elem:
        trading_stats['average_loss'] = avg_loss_elem.text.strip()

    data['trading_statistics'] = trading_stats

    # --- 5. Additional Stats ---
    additional_stats = {}
    trades_week_elem = soup.find('div', attrs={'automation-id': 'stats-trading-trades-per-week-value'})
    if trades_week_elem:
        additional_stats['trades_per_week'] = trades_week_elem.text.strip()
    
    holding_time_elem = soup.find('div', attrs={'automation-id': 'stats-trading-avg-holding-time-value'})
    if holding_time_elem:
        additional_stats['average_holding_time'] = holding_time_elem.text.strip()
        
    active_since_elem = soup.find('div', attrs={'automation-id': 'stats-trading-active-since-value'})
    if active_since_elem:
        additional_stats['account_active_since'] = active_since_elem.text.strip()

    # Profitable weeks
    profitable_weeks_elem = soup.find('div', attrs={'automation-id': 'stats-chart-profitable-weeks-parameter'})
    if profitable_weeks_elem:
         val = profitable_weeks_elem.find('span', class_='data-value')
         if val:
             additional_stats['profitable_weeks'] = val.text.strip()

    data['additional_stats'] = additional_stats

    # --- 6. ESG Rating ---
    esg = {}
    esg_score_elem = soup.find('div', attrs={'automation-id': 'user-stats-esg-score-value'})
    if esg_score_elem:
        esg['overall_score'] = esg_score_elem.text.strip()
    
    # Sub-scores (Environmental, Social, Governance)
    # These are often in a list under the main score
    esg_list = soup.find('div', class_='esg-breakdown-list') # Hypothetical class
    if not esg_list:
        # Try finding by label
        for cat in ['Environmental', 'Social', 'Governance']:
            cat_elem = soup.find(string=cat)
            if cat_elem:
                # Value is usually nearby
                parent = cat_elem.find_parent('div')
                if parent:
                    val = parent.find_next_sibling('div') or parent.find('span', class_='value')
                    if val:
                        esg[cat.lower()] = val.text.strip()

    data['esg_rating'] = esg

    return data

def generate_stats_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_stats_markdown(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# User Statistics\n\n")
        
        # Helper to write a section table
        def write_section(title, section_data):
            if not section_data:
                return
            f.write(f"## {title}\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            for k, v in section_data.items():
                if isinstance(v, dict):
                    # Handle nested dicts like user_vs_spx500
                    val_str = ", ".join([f"{sub_k}: {sub_v}" for sub_k, sub_v in v.items()])
                    f.write(f"| {k.replace('_', ' ').title()} | {val_str} |\n")
                else:
                    f.write(f"| {k.replace('_', ' ').title()} | {v} |\n")
            f.write("\n")

        write_section("Performance", data.get('performance'))
        write_section("Asset Allocation", data.get('asset_allocation'))
        write_section("Dividends", data.get('dividends'))
        write_section("Trading Statistics", data.get('trading_statistics'))
        write_section("Additional Stats", data.get('additional_stats'))
        write_section("ESG Rating", data.get('esg_rating'))
