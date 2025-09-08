# Django + Selenium Scraper Demo

A small Django project showcasing a Selenium-based web scraper with:
- Headless Chrome (via webdriver-manager)
- A management command (`run_scrape`) to run from CLI
- A simple web UI to trigger a scrape and display JSON results

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install "Django>=5,<6" selenium webdriver-manager python-dotenv
```

## Run the site

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Navigate to `http://localhost:8000` and click "Run Scrape".

## Run the scraper via CLI

```bash
python manage.py run_scrape
```

## Notes
- Uses Selenium test page at `https://www.selenium.dev/selenium/web/web-form.html`.
- Headless Chrome is configured for CI/WSL. If Chrome is not installed, install Google Chrome or Chromium.
- WebDriver is auto-managed by `webdriver-manager`.
