from rest_framework import serializers
from .models import Job, Application

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'location', 'salary']
        read_only_fields = ['created_by', 'created_at',]  # Prevent modification


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'user', 'job', 'cover_letter', 'applied_at']
