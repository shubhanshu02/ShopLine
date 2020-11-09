from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Notification, Seller, Item, BillItem
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
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
    return render(request, 'shop/dashboard_home.html', {'seller': seller})


@csrf_exempt
def bill_generate(request):
    if request.user.is_authenticated:
        seller = Seller.objects.filter(user=request.user)[0]
        item = Item.objects.filter(seller=seller)
        if request.method == 'GET':
            forjs = item.values_list()
            forjs = json.dumps(list(forjs), cls=DjangoJSONEncoder)
            print(forjs)
            if item.count() > 0:
                return render(request, 'shop/bill_generation.html', {'items': item, 'itm': forjs})
            return render(request, 'shop/bill_generation.html', {'message': "No Product to show"})

        elif request.method == 'POST':
            item = list(item)
            data = json.loads(request.body)
            amt_list = data['items'][0]
            print('\n\n\n\n\n\n', amt_list, '\n\n\n')
            billItems = []
            for i in range(len(amt_list)):
                if amt_list[i] != 0:
                    print('\t\t', item[i-1].pk)
                    t = BillItem(item=item[i-1].pk, price=item[i-1].price,
                                 quantity=amt_list[i-1], total=amt_list[i-1]*item[i-1].price)
                    billItems.append(t)
            # Add Bill Object and save bill items
            return JsonResponse({'status': 'ok'})

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
