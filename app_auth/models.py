from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms


ROLE_CHOICES = [
    ("Teacher", "Teacher"),
    ("Student", "Student"),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_logged_in = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Student")

    def __str__(self):
        return f"Profile of {self.user.username} ({self.role})"
