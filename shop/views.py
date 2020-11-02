from django.shortcuts import render
from .models import Notification, Seller, Item
import datetime
# Create your views here.


def home(request):
    return render(request, 'shop/index.html')


def dashboard(request):
    return render(request, 'shop/dashboard.html')


def notifications(request):
    sel = Seller.objects.filter(user = request.user)[0]
    for i in range(10):
        nam = f'Item ${i}'
        Item(name = nam, price=  10, size= '500ml',quantity_available= 50,min_quantity=i+10, seller = sel).save()


    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        if (notifications.count() == 0):
            return render(request, 'shop/notifications.html', {'message': "Nothing to Show"})
        return render(request, 'shop/notifications.html', {'noti': notifications})
    return render(request, 'shop/notifications.html', {'message': "You must be logged in to see this page"})
