from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, Category

class TaskAPITestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.category = Category.objects.create(name='Work', description='Work related tasks')
        self.task_data = {
            'title': 'Test Task',
            'description': 'Testing API',
            'status': 'pending',
            'priority': 2,
            'category_id': self.category.id
        }
        
    def test_create_task_unauthenticated(self):
        """Test that unauthenticated users cannot create tasks"""
        response = self.client.post('/api/tasks/', self.task_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_task_authenticated(self):
        """Test authenticated user can create task"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/tasks/', self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')
    
    def test_list_tasks(self):
        """Test listing tasks"""
        self.client.force_authenticate(user=self.user)
        Task.objects.create(
            title='Task 1',
            description='First task',
            created_by=self.user,
            category=self.category
        )
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_complete_task(self):
        """Test complete action"""
        self.client.force_authenticate(user=self.user)
        task = Task.objects.create(
            title='Complete me',
            description='Should be completed',
            created_by=self.user
        )
        response = self.client.post(f'/api/tasks/{task.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')
    
    def test_dashboard_stats(self):
        """Test dashboard endpoint"""
        self.client.force_authenticate(user=self.user)
        Task.objects.create(
            title='Task 1',
            status='pending',
            created_by=self.user
        )
        Task.objects.create(
            title='Task 2',
            status='completed',
            created_by=self.user
        )
        response = self.client.get('/api/tasks/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 2)
        self.assertEqual(response.data['completed'], 1)
        self.assertEqual(response.data['pending'], 1)