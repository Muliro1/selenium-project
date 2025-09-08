def test_firefox_scraper():
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager
    
    options = FirefoxOptions()
    options.add_argument('--headless')
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        driver.get("https://www.google.com")
        return driver.title
    finally:
        driver.quit()
