from rest_framework import serializers
from .models import Task

# LEVEL 1: Basic Serializer (manual fields)
class BasicTaskSerializer(serializers.Serializer):
    """Manual serializer - full control but more code"""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=['pending', 'in_progress', 'completed'])
    
    def create(self, validated_data):
        """How to create an object"""
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """How to update an object"""
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

# LEVEL 2: ModelSerializer (recommended)
class TaskSerializer(serializers.ModelSerializer):
    """Auto-generates fields from model - much less code"""
    
    # Custom field (not in model)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'is_overdue']
        read_only_fields = ['id', 'created_at']
    
    def get_is_overdue(self, obj):
        """Custom logic for SerializerMethodField"""
        from django.utils import timezone
        if obj.status != 'completed':
            days_old = (timezone.now() - obj.created_at).days
            return days_old > 7
        return False
    
    # Field-level validation
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")
        if Task.objects.filter(title=value).exists():
            raise serializers.ValidationError("Task with this title already exists")
        return value
    
    # Object-level validation (multiple fields)
    def validate(self, data):
        if data.get('status') == 'completed' and not data.get('description'):
            raise serializers.ValidationError({
                'description': 'Completed tasks must have a description'
            })
        return data

# LEVEL 3: Nested Serializer (for relationships)
class TaskSummarySerializer(serializers.ModelSerializer):
    """Minimal fields for list views"""
    class Meta:
        model = Task
        fields = ['id', 'title', 'status']