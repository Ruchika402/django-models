from django.contrib import admin
from .models import Task
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['title']