from django.core.management.base import BaseCommand
from scraper.scraper import scrape_github_trending
import json

class Command(BaseCommand):
    help = 'Scrape GitHub trending repos'
    
    def handle(self, *args, **options):
        result = scrape_github_trending()
        self.stdout.write(json.dumps(result, indent=2))
