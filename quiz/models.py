from django.db import models
from rest_framework import serializers


class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField(default=list)  # default to empty list
    answer = models.PositiveIntegerField(default=0)  # default to index 0

    def __str__(self):
        return self.text

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.text,
            "options": self.options,
            "answer": self.answer
        }

class Session(models.Model):
    quiz_id = models.CharField(max_length=100, unique=True)
    data = models.JSONField(default=dict)  # stores questions with answers (or whole quiz)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"sessions {self.quiz_id}"


