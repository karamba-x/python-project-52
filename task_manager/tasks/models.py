from django.contrib.auth.models import User
from django.db import models
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='tasks')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executed_tasks', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
