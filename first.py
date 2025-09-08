from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import shutil
import tempfile
import time


def resolve_chrome_binary():
    for key in ("CHROME_BINARY", "GOOGLE_CHROME_BIN", "CHROMIUM_BINARY"):
        val = os.environ.get(key)
        if val and os.path.exists(val):
            return val
    for name in ("google-chrome", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return path
    return None


opts = Options()
opts.add_argument('--headless=new')  # Comment out to see browser window
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--disable-gpu')
opts.add_argument('--disable-extensions')
opts.add_argument('--remote-debugging-port=0')
opts.add_argument('--no-zygote')
opts.add_argument('--window-size=1920,1080')
profile_dir = tempfile.mkdtemp(prefix='selenium-profile-')
opts.add_argument(f'--user-data-dir={profile_dir}')
opts.add_argument(f'--data-path={tempfile.mkdtemp(prefix="chrome-data-")}')
opts.add_argument(f'--disk-cache-dir={tempfile.mkdtemp(prefix="chrome-cache-")}')

binary = resolve_chrome_binary()
if binary:
    opts.binary_location = binary

use_chromium = bool(binary and 'chromium' in os.path.basename(binary))
manager = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM) if use_chromium else ChromeDriverManager()
service = Service(manager.install())
driver = webdriver.Chrome(service=service, options=opts)

driver.get("https://www.google.com")
#print(driver.title)
input_box = driver.find_element(By.CLASS_NAME, "gLFyf")
input_box.send_keys("selenium")
input_box.send_keys(Keys.ENTER)

driver.quit()