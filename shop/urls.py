from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('notifications', views.notifications, name='notifications'),
]