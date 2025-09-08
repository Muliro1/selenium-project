from typing import Dict, Any
import os
import shutil
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _resolve_chrome_binary() -> str | None:
    # Prefer explicit env vars
    for env_key in ('CHROME_BINARY', 'GOOGLE_CHROME_BIN', 'CHROMIUM_BINARY'):
        val = os.environ.get(env_key)
        if val and os.path.exists(val):
            return val
    # Try common executables on Linux
    for name in ('google-chrome', 'chromium', 'chromium-browser'):
        path = shutil.which(name)
        if path:
            return path
    return None


def _build_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--no-zygote')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--remote-allow-origins=*')
    # Use a dedicated profile dir to avoid DevToolsActivePort conflicts
    user_data_dir = tempfile.mkdtemp(prefix='chrome-profile-')
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    # Additional temp dirs to avoid permission issues in WSL/CI
    chrome_options.add_argument(f'--data-path={tempfile.mkdtemp(prefix="chrome-data-")}')
    chrome_options.add_argument(f'--disk-cache-dir={tempfile.mkdtemp(prefix="chrome-cache-")}')
    if os.environ.get('CI'):
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    binary = _resolve_chrome_binary()
    if binary:
        chrome_options.binary_location = binary
    # Use Chromium driver if the binary is Chromium
    use_chromium = bool(binary and 'chromium' in os.path.basename(binary))
    manager = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM) if use_chromium else ChromeDriverManager()
    service = Service(manager.install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(1.0)
    return driver


def run_demo_scrape() -> Dict[str, Any]:
    url = 'https://www.selenium.dev/selenium/web/web-form.html'
    driver = _build_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.title_contains('Web form'))
        title = driver.title
        text_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'my-text'))
        )
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button'))
        )
        text_box.send_keys('Selenium')
        submit_button.click()
        message_el = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'message'))
        )
        message = message_el.text
        return {
            'url': url,
            'title': title,
            'message': message,
        }
    finally:
        driver.quit()

def scrape_github_trending():
    driver = _build_driver()
    try:
        driver.get("https://github.com/trending")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Box-row")))
        
        repos = driver.find_elements(By.CLASS_NAME, "Box-row")[:10]  # Top 5
        results = []
        for repo in repos:
            name = repo.find_element(By.CSS_SELECTOR, "h2 a").text.strip()
            stars = repo.find_element(By.CSS_SELECTOR, "[href*='/stargazers']").text.strip()
            results.append({"name": name, "stars": stars})
        
        return {"trending_repos": results}
    finally:
        driver.quit()

def scrape_with_screenshot(url):
    driver = _build_driver()
    try:
        driver.get(url)
        driver.save_screenshot(f'/tmp/screenshot_{int(time.time())}.png')
        return {
            'url': url,
            'title': driver.title,
            'screenshot_saved': True
        }
    finally:
        driver.quit()





