from django.db import models
from labels.models import Label
from django.contrib.auth.models import User
from statuses.models import Status  # Assuming Statuses is a model in statuses app
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')  # ForeignKey to Statuses model
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='authored_tasks')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')  # Assuming creator is a username
    tags = models.ManyToManyField(Label, blank=True, related_name='tasks')  # Many-to-many relationship  Label
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


