from django.shortcuts import render
from .models import Notification, Seller, Item
import datetime
# Create your views here.


def home(request):
    return render(request, 'shop/index.html')


def dashboard(request):
    if request.user.is_authenticated:
        seller = Seller.objects.filter(user=request.user)[0]
        item = Item.objects.filter(seller=seller)
        if item.count() > 0:
            return render(request, 'shop/Item_Available.html', {'items': item})
        return render(request, 'shop/Item_Available.html', {'message': "No Product to show"})
    return render(request, 'shop/Item_Available.html', {'message': "Please Login to View this Page"})


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        if (notifications.count() > 0):
            return render(request, 'shop/notifications.html', {'noti': notifications})
        return render(request, 'shop/notifications.html', {'message': "Nothing to Show"})
    return render(request, 'shop/notifications.html', {'message': "You must be logged in to see this page"})
