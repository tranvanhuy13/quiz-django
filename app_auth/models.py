from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_logged_in = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Profile of {self.user.username}"
