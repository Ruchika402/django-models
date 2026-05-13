from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend  # pip install django-filter
from .models import Task
from .serializers import TaskSerializer

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    #filetring
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']

    #custom action: mark task as complete
    @action(detail = True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response({
            'status': 'completed',
            'task': TaskSerializer(task).data
        })
        # Custom action: bulk delete pending tasks
    @action(detail=False, methods=['delete'])
    def delete_pending(self, request):
        deleted_count, _ = Task.objects.filter(status='pending').delete()
        return Response({'deleted_count': deleted_count})
    
    # Override create to add custom logic
    def create(self, request, *args, **kwargs):
        print(f"Creating task with data: {request.data}")  # Custom logging
        return super().create(request, *args, **kwargs)
    
    @action(detail=False,methods = ['get'])
    def completed(self,request):
        completed_tasks = Task.objects.filter(status='completed')
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)
    
       # NEW: Get task statistics
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get task statistics"""
        total = Task.objects.count()
        completed = Task.objects.filter(status='completed').count()
        pending = Task.objects.filter(status='pending').count()
        in_progress = Task.objects.filter(status='in_progress').count()
        
        return Response({
            'total_tasks': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'completion_rate': round((completed/total)*100, 2) if total > 0 else 0
        })