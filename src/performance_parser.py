import json
from bs4 import BeautifulSoup

def extract_performance_data(html_content):
    """
    Parses the HTML of an eToro user's main profile page to extract yearly performance data
    and additional metrics.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # --- Extract Annual Performance ---
    annual_performance = []
    # Find all the candle containers, which represent yearly performance
    # Note: The provided example uses 'div' for automation_id='stats-chart-full-month'
    # but we should be flexible if it's a different tag, though attrs usually works best.
    candles = soup.find_all('div', attrs={'automation-id': 'stats-chart-full-month'})

    for candle in candles:
        # The tooltip contains the precise values
        gain_tooltip = candle.find('div', attrs={'automation-id': 'stats-chart-gain-tooltip'})
        
        if gain_tooltip:
            gain_loss_span = gain_tooltip.find('span', class_='tooltip-number')
            year_span = gain_tooltip.find('span', class_='tooltip-date')
            
            if gain_loss_span and year_span:
                gain_loss = gain_loss_span.text.strip()
                year = year_span.text.strip()
                annual_performance.append({"year": year, "gainLoss": gain_loss})
    
    # --- Extract Additional Metrics ---
    additional_metrics = {}
    
    # Rendite YTD
    rendite_ytd_span = soup.find('span', attrs={'automation-id': 'return-ytd-data-value-parameter'})
    if rendite_ytd_span:
        additional_metrics['renditeYTD'] = rendite_ytd_span.text.strip()
        
    # Rendite 2Y
    rendite_2y_span = soup.find('span', attrs={'automation-id': 'return-2y-data-value-parameter'})
    if rendite_2y_span:
        additional_metrics['rendite2Y'] = rendite_2y_span.text.strip()
        
    # Average Risk Rating
    # This is often in a div with class 'risk-default'
    risk_div = soup.find('div', class_='risk-default')
    if risk_div:
        additional_metrics['averageRiskRatingLast7Days'] = risk_div.text.strip()
        
    # Profitable Weeks
    profitable_weeks_container = soup.find('div', attrs={'automation-id': 'stats-chart-profitable-weeks-parameter'})
    if profitable_weeks_container:
        profitable_weeks_span = profitable_weeks_container.find('span', class_='data-value')
        if profitable_weeks_span:
            additional_metrics['profitableWeeks'] = profitable_weeks_span.text.strip()

    return {
        "annualPerformance": annual_performance,
        "additionalMetrics": additional_metrics
    }

def generate_performance_json(data, output_path):
    """
    Generates a JSON file from the performance data.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_performance_markdown(data, output_path):
    """
    Generates a Markdown file with tables for performance data and metrics.
    """
    if not data:
        return

    with open(output_path, 'w', encoding='utf-8') as f:
        # Annual Performance Table
        f.write("### Annual Performance\n\n")
        f.write("| Year | Gain/Loss |\n")
        f.write("|------|-----------|\n")
        
        annual_perf = data.get('annualPerformance', [])
        if annual_perf:
            for item in annual_perf:
                f.write(f"| {item.get('year', '—')} | {item.get('gainLoss', '—')} |\n")
        else:
            f.write("| — | — |\n")
            
        f.write("\n")
        
        # Additional Metrics Table
        f.write("### Additional Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        
        metrics = data.get('additionalMetrics', {})
        if metrics:
            # Map keys to readable names
            key_map = {
                'renditeYTD': 'Rendite YTD',
                'rendite2Y': 'Rendite 2Y',
                'averageRiskRatingLast7Days': 'Durchschnittliche Risikobewertung (letzte 7T)',
                'profitableWeeks': 'Gewinnbringende Wochen'
            }
            
            for key, value in metrics.items():
                readable_name = key_map.get(key, key)
                f.write(f"| {readable_name} | {value} |\n")
        else:
            f.write("| — | — |\n")
