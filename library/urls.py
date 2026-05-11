from django.urls import path
from library import views

urlpatterns = [
    path('stats/',views.stats_dashboard,name = 'stats'),
    path('book/<int:book_id>/review/', views.book_review, name='book_review'),
    path('book/', views.book_management, name='book_management'), 
]


    

