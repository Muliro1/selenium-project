from django.test import TestCase
from scraper.scraper import run_demo_scrape, scrape_github_trending


class ScraperTitleTest(TestCase):
    def test_title_contains_web_form(self):
        result = run_demo_scrape()
        self.assertIn('Web form', result['title'])

class ScraperTests(TestCase):
    def test_selenium_form_submission(self):
        result = run_demo_scrape()
        self.assertIn('Web form', result['title'])
        self.assertIn('Received!', result['message'])
    
    def test_github_trending_has_repos(self):
        result = scrape_github_trending()
        self.assertIn('trending_repos', result)
        self.assertGreater(len(result['trending_repos']), 0)
    
    def test_scraper_returns_dict(self):
        result = run_demo_scrape()
        self.assertIsInstance(result, dict)
        self.assertIn('url', result)
        self.assertIn('title', result) 