from django.core.management.base import BaseCommand
from scraper.scraper import run_demo_scrape
import json


class Command(BaseCommand):
    help = 'Run the demo Selenium scraper and print JSON output.'

    def handle(self, *args, **options):
        result = run_demo_scrape()
        self.stdout.write(json.dumps(result, indent=2))


