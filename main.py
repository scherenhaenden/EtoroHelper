import os
import argparse
from datetime import datetime
from src.dependencies import install_dependencies
from src.url_utils import extract_username_from_url, validate_username

def main():
    parser = argparse.ArgumentParser(description='EtoroHelper - Extract and parse eToro data')
    parser.add_argument('--user', type=str, help='eToro username directly (e.g., scherenhaenden)')
    parser.add_argument('--user-url', type=str, help='eToro user profile URL (e.g., https://www.etoro.com/people/username)')
    parser.add_argument('--base-dir', type=str, help='Base directory for input/output (default: current date)')

    args = parser.parse_args()

    # Determine base directory
    if args.base_dir:
        base_dir = args.base_dir
    else:
        base_dir = datetime.now().strftime('%Y-%m-%d')

    # Extract username from arguments or fallback sources
    username = None

    # Priority 1: --user (direct username)
    if args.user:
        try:
            username = validate_username(args.user)
            print(f"Using username: {username}")
        except ValueError as e:
            print(f"Error with username: {e}")
            return

    # Priority 2: --user-url (extract from URL)
    if not username and args.user_url:
        try:
            username = extract_username_from_url(args.user_url)
            print(f"Extracted username from URL: {username}")
        except ValueError as e:
            print(f"Error parsing URL: {e}")
            return

    # Install all dependencies first
    install_dependencies()

    # Import modules after dependencies are confirmed
    from src.parser import extract_portfolio_data, generate_json, generate_markdown
    from src.downloader import download_person_data
    from src.performance_parser import extract_performance_data as extract_person_performance
    from src.performance_parser import generate_performance_json, generate_performance_markdown
    from src.stats_parser import extract_stats_data, generate_stats_json, generate_stats_markdown

    # Base directory for the current run
    # base_dir = "2025-12-15"

    # --- Part 1: Parse local portfolio file ---
    input_dir = os.path.join(base_dir, "input")
    if os.path.exists(input_dir):
        output_dir = os.path.join(base_dir, "output")
        
        input_file = None
        for file in os.listdir(input_dir):
            if file.endswith(('.txt', '.html')):
                input_file = os.path.join(input_dir, file)
                break

        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            portfolio = extract_portfolio_data(html_content)

            os.makedirs(output_dir, exist_ok=True)
            generate_json(portfolio, os.path.join(output_dir, 'portfolio.json'))
            generate_markdown(portfolio, os.path.join(output_dir, 'portfolio.md'))
            print("Portfolio parsing complete. Outputs generated.")
        else:
            print("No input file found in 'input' directory for parsing.")

    # --- Part 2: Download and Parse Person Data ---
    # Check if we have a username from arguments or from legacy person.txt file
    person = username
    if not person:
        person_portfolio_dir = os.path.join(base_dir, "portfolio")
        if os.path.exists(person_portfolio_dir):
            person_file = os.path.join(person_portfolio_dir, 'person.txt')
            if os.path.exists(person_file):
                with open(person_file, 'r') as f:
                    person = f.read().strip()

    if person:
        # Downloads go to ./downloads/{user}/{yyyy-MM-dd}/
        download_dir = os.path.join('downloads', person, datetime.now().strftime('%Y-%m-%d'))

        print(f"\nStarting person data download for {person}...")
        print(f"Saving to: {download_dir}")
        download_person_data(person, download_dir)
        print("Person data download process complete.")

        person_output_dir = download_dir

        # Parse Performance Data
        profile_html_path = os.path.join(person_output_dir, 'profile.html')
        if not os.path.exists(profile_html_path):
            profile_html_path = os.path.join(person_output_dir, f'{person}.html') # Fallback

        if os.path.exists(profile_html_path):
            print(f"Parsing performance data for {person}...")
            with open(profile_html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            performance_data = extract_person_performance(html_content)
            generate_performance_json(performance_data, os.path.join(person_output_dir, 'performance.json'))
            generate_performance_markdown(performance_data, os.path.join(person_output_dir, 'performance.md'))
            print(f"Performance data for {person} parsed and saved.")
        else:
            print(f"Could not find profile HTML for {person} to parse.")

        # Parse Stats Data
        stats_html_path = os.path.join(person_output_dir, 'stats.html')
        if os.path.exists(stats_html_path):
            print(f"Parsing stats data for {person}...")
            with open(stats_html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            stats_data = extract_stats_data(html_content)
            generate_stats_json(stats_data, os.path.join(person_output_dir, 'stats.json'))
            generate_stats_markdown(stats_data, os.path.join(person_output_dir, 'stats.md'))
            print(f"Stats data for {person} parsed and saved.")
        else:
            print(f"Could not find stats HTML for {person} to parse.")
    else:
        print("No username provided via --user, --user-url or person.txt file found.")


if __name__ == "__main__":
    main()
