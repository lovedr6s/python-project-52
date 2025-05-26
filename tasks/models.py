from django.db import models
from labels.models import Label
from django.contrib.auth.models import User
from statuses.models import Status  # Assuming Statuses is a model in statuses app
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Statuses model
    author = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Assuming creator is a username
    tags = models.ManyToManyField(Label, blank=True)  # Many-to-many relationship  Label
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
