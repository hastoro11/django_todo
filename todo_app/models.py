from django.db import models
from django.contrib.auth.models import User


class TODO(models.Model):
    title = models.CharField(max_length=128)
    completed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title