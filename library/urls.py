from django.urls import path
from library import views

urlpatterns = {
    path('stats/',views.stats_dashboard,name = 'stats'),
     path('book/<int:book_id>/reviews/', views.book_reviews, name='book_reviews')

}