from django.shortcuts import render
from .models import Notification, Seller, Item
import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


def home(request):
    return render(request, 'shop/index.html')


def stock(request):
    if request.user.is_authenticated:
        seller = Seller.objects.filter(user=request.user)[0]
        item = Item.objects.filter(seller=seller)
        if item.count() > 0:
            return render(request, 'shop/item_Available.html', {'items': item})
        return render(request, 'shop/item_Available.html', {'message': "No Product to show"})
    return render(request, 'shop/item_Available.html', {'message': "Please Login to View this Page"})

def dashboard(request):
    seller = None
    if request.user.is_authenticated:
        seller = Seller.objects.filter(user=request.user)[0]
    return render(request, 'shop/dashboard_home.html', {'seller':seller })

def bill_generate(request):
    if request.user.is_authenticated:
        seller = Seller.objects.filter(user=request.user)[0]
        item = Item.objects.filter(seller=seller)
        forjs = item.values_list()
        forjs = json.dumps(list(forjs), cls=DjangoJSONEncoder)

        print(forjs)
        if item.count() > 0:
            return render(request, 'shop/bill_generation.html', {'items': item, 'itm':forjs})
        return render(request, 'shop/bill_generation.html', {'message': "No Product to show"})
    return render(request, 'shop/bill_generation.html', {'message': "Please Login to View this Page"})

    

def update_stock(request):
    return render(request, 'shop/update_stock.html')


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        if (notifications.count() > 0):
            return render(request, 'shop/notifications.html', {'noti': notifications})
        return render(request, 'shop/notifications.html', {'message': "Nothing to Show"})
    return render(request, 'shop/notifications.html', {'message': "You must be logged in to see this page"})
