from django.db import models
from labels.models import Label  # Assuming Label model is in labels app
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    tags = models.ManyToManyField(Label, blank=True)  # Many-to-many relationship  Label
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
