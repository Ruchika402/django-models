from rest_framework import serializers
from .models import Task,Category
from django.contrib.auth.models import User
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username','email','full_name']
    def get_full_name(self,obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'task_count']
        read_only_fields = ['created_at']
    
    def get_task_count(self, obj):
        return obj.tasks.count()

class TaskSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'category_name','assigned_to_username','created_at', 'updated_at', 'days_since_created']
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