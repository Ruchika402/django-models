from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
   
   
    
    # NEW URLs for today's lesson
    path('filter/', views.book_filter_view, name='book_filter'),  # Main filter page
    path('filter-demo/', views.filter_demo_view, name='filter_demo'),  # Educational demo
]