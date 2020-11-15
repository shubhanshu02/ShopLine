from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/stock', views.stock, name='Available Stock'),
    path('dashboard/bill', views.bill_generate, name='Bill Generation'),
    path('dashboard/update', views.update_stock, name='Update Stock'),
    path('notifications', views.notifications, name='notifications'),
    path('dashboard/add',views.newItem,name="New Item")
]