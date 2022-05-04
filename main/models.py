from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    published_year = models.CharField(max_length=10)
    external_id = models.CharField(max_length=50)
    acquired = models.BooleanField()
    thumbnail = models.CharField(max_length=200, blank=True)
    
    
    def __str__(self):
        return self.title
    
