from django.urls import path
from authentication.views import *
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('register', signup,name='register'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
]
