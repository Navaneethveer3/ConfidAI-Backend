from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    QUESTION_TYPES = [
        ('general', 'General'),
        ('skill', 'Skill-based'),
        ('project', 'Project-based'),
    ]

    text = models.TextField()
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    skill = models.CharField(max_length=100, blank=True, null=True)  # Only for skill-based questions
    type = models.CharField(max_length=100, null=True, blank=True,default="skill")
    is_project_related = models.BooleanField(default=False)  # True if it's a project-based question


    def __str__(self):
        return self.text

class InterviewSession(models.Model):
    user_id = models.CharField(max_length=255)  # Firebase User ID
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)  # Store overall confidence score
    feedback = models.TextField(blank=True)  # Store feedback for improvements

    def __str__(self):
        return f"Interview Session - {self.user_id} ({self.started_at})"


class Answer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    confidence_level = models.FloatField(default=0.0)  # Store confidence score
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer in Session {self.session.id} - {self.question[:50]}"


class UserResponse(models.Model):
    user_id = models.CharField(max_length=255)  # Firebase User ID
    question = models.TextField()
    answer = models.TextField()
    confidence_level = models.FloatField(default=0.0)  # Store confidence score
    facial_expression = models.CharField(max_length=255, null=True, blank=True)  # Store facial emotion
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user_id} - {self.question[:50]}"