from django.urls import path
from library import views

urlpatterns = {
    path('stats/',views.stats_dashboard,name = 'stats')

}