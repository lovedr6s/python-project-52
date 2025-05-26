from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
