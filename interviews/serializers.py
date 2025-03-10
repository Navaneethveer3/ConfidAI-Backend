from rest_framework import serializers
from .models import InterviewSession

class InterviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSession
        fields = ["id", "user_id", "started_at", "completed_at", "confidence_score", "feedback"]
