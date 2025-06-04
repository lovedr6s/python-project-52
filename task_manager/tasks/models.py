from django.db import models
from task_manager.labels.models import Label
from django.contrib.auth.models import User
from task_manager.statuses.models import Status  # Assuming Statuses is a model in statuses app
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')  # ForeignKey to Statuses model
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='author')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='executor')  # Assuming creator is a username
    tags = models.ManyToManyField(Label, blank=True, related_name='tags')  # Many-to-many relationship  Label
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


