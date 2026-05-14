from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),('in_progress','In Progress'),('completed','Completed'),
    ]
    PROIRITY_CHOICES = [(1,'Low'),(2,'Medium'),(3,'High'),(4,'Urgent'),]
    title = models.CharField(max_length = 100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null = True,blank = True)
    

    category = models.ForeignKey(Category, on_delete=models.SET_NULL , null = True,blank = True,related_name ='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and self.status != 'completed':
            return self.due_date < timezone.now()
        return False




