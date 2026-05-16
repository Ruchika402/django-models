from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from .pagination import StandardResultsSetPagination
from .permissions import IsAssignedOrCreator, IsOwnerOrReadOnly
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    # Dynamic serializer based on action
    def get_serializer_class(self):
        if self.action == 'list':
            return TaskSerializer  # Lighter serializer for list views
        return TaskSerializer
    
    #filetring
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category__name', 'assigned_to__id']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'updated_at']
    ordering = ['-created_at']  # Default ordering

    #custom action: mark task as complete
    def get_queryset(self):
        """Filter tasks based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        # Non-authenticated users see only public info
        if not user.is_authenticated:
            return queryset.none()
        
        # Users see their own tasks and tasks assigned to them
        return queryset.filter(
            Q(created_by=user) | Q(assigned_to=user)
        )
   
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @method_decorator(vary_on_headers('Authorization'))
    def list(self, request, *args, **kwargs):
        """Cached list endpoint"""
        return super().list(request, *args, **kwargs)
    # Custom action: Get user's dashboard stats
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def dashboard(self, request):
        """Cached dashboard data"""
        user_id = request.user.id
        cache_key = f'dashboard_{user_id}'
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Calculate fresh data
        from django.utils import timezone
        tasks = Task.objects.filter(created_by=request.user)
        
        stats = {
            'total': tasks.count(),
            'completed': tasks.filter(status='completed').count(),
            'completion_rate': self._calculate_rate(tasks),
            'overdue': tasks.filter(due_date__lt=timezone.now()).count(),
        }
        
        # Store in cache for 5 minutes
        cache.set(cache_key, stats, timeout=300)
        
        return Response(stats)
    @action(detail=False, methods=['post'])
    def invalidate_cache(self, request):
        """Clear user's dashboard cache"""
        cache_key = f'dashboard_{request.user.id}'
        cache.delete(cache_key)
        return Response({'message': 'Cache cleared'})
    # Custom action: Mark task as complete
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a specific task as completed"""
        task = self.get_object()
        task.status = 'completed'
        task.save()
        return Response({'status': 'completed', 'task_id': task.id})
    
   
     
    # Custom action: Bulk update status
    @action(detail=False, methods=['post'])
    def bulk_update_status(self, request):
        """Update multiple tasks at once"""
        task_ids = request.data.get('task_ids', [])
        new_status = request.data.get('status')
        
        if not task_ids or not new_status:
            return Response(
                {'error': 'task_ids and status are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_count = Task.objects.filter(id__in=task_ids).update(status=new_status)
        
        return Response({
            'updated_count': updated_count,
            'status': new_status,
            'message': f'Updated {updated_count} tasks to {new_status}'
        })
class TaskViewSet(viewsets.ModelViewSet):
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        # Clear cache after creating
        self._clear_user_cache()
    
    def perform_update(self, serializer):
        serializer.save()
        self._clear_user_cache()
    
    def perform_destroy(self, instance):
        instance.delete()
        self._clear_user_cache()
    
    def _clear_user_cache(self):
        cache_key = f'dashboard_{self.request.user.id}'
        cache.delete(cache_key)
class CategoryViewSet(viewsets.ModelViewSet):
    """Category CRUD operations"""
    queryset = Category.objects.prefetch_related('tasks').all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """Get all tasks in a category"""
        category = self.get_object()
        tasks = category.tasks.all()
        
        # Apply task filters
        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)
    



from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
