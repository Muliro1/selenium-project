from django.db import models

# Create your models here.
from django.db import models

class ScrapeResult(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.scraped_at}"

