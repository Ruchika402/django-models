from rest_framework import serializers
from .models import Task
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 
                  'created_at', 'updated_at', 'days_since_created']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_days_since_created(self,obj):
        delta = timezone.now() - obj.created_at
        return delta.days
    
    def validate_title(self, value):
        if len(value)<3:
            raise serializers.ValidationError("title must be at least 3 characters")
        return value
    
    def validate(self,data):
        if data.get('status') == 'completed' and not data.get('description'):
            raise serializers.ValidationError("Completed tasks need a description")
        return data