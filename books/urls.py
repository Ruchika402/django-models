from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
   
   
    
    
    path('filter/', views.book_filter_view, name='book_filter'),
    path('filter-demo/', views.filter_demo_view, name='filter_demo'),
    
    # NEW URLs for today's lesson
    path('advanced-search/', views.advanced_search_view, name='advanced_search'),
    path('search-bar/', views.search_bar_view, name='search_bar'),
    path('get-vs-filter/', views.get_vs_filter_demo, name='get_vs_filter_demo'),
]