import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def download_person_data(person, download_dir):
    """
    Download eToro profile pages for a given user.

    Args:
        person: eToro username (e.g. 'scherenhaenden')
        download_dir: Directory where the downloaded HTML files will be saved
                      (e.g. './downloads/scherenhaenden/2026-02-23')
    """
    if not person:
        raise ValueError("person must be a non-empty username")
    if not download_dir:
        raise ValueError("download_dir must be a non-empty path")

    urls = [
        (f"https://www.etoro.com/people/{person}", "profile"),
        (f"https://www.etoro.com/people/{person}/stats", "stats"),
        (f"https://www.etoro.com/people/{person}/portfolio", "portfolio"),
        (f"https://www.etoro.com/people/{person}/chart", "chart")
    ]

    wait_selectors = {
        "profile": '[automation-id="user-stats-chart-container"]',
        "stats": 'et-card-content',
        "portfolio": 'et-portfolio-group-list',
        "chart": 'et-chart-container',
    }

    output_dir = download_dir
    os.makedirs(output_dir, exist_ok=True)

    # Setup selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure Google Chrome is installed.")
        return

    try:
        for url, page_type in urls:
            try:
                print(f"Downloading {url} with Selenium...")
                driver.get(url)

                selector = wait_selectors.get(page_type)
                if selector:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )

                # Give late-loaded sections a chance to render.
                time.sleep(5)

                html_content = driver.page_source
                file_path = os.path.join(output_dir, f"{page_type}.html")

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"Successfully downloaded and saved to {file_path}")

            except Exception as e:
                print(f"Failed to download {url}: {e}")
                # Save what we have for debugging.
                try:
                    file_path = os.path.join(output_dir, f"{page_type}_failed.html")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    print(f"Saved partial content to {file_path}")
                except Exception:
                    pass
    finally:
        if driver is not None:
            driver.quit()
