from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Notification, Seller, Item, BillItem, Bill
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now
from django.http import HttpResponse
from django.utils import datetime_safe
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
    old_bills = None
    if request.user.is_authenticated:
        seller = Seller.objects.filter(user=request.user)[0]
        old_bills = Bill.objects.filter(seller=seller)
    return render(request, 'shop/dashboard_home.html', {'seller': seller,'old_bills':old_bills})


@csrf_exempt
def bill_generate(request):
    if request.user.is_authenticated:
        current_seller = Seller.objects.get(user=request.user)
        item_query = Item.objects.filter(seller=current_seller)

        if request.method == 'GET':
            items_json = item_query.values_list()
            items_json = json.dumps(list(items_json), cls=DjangoJSONEncoder)
            if item_query.count() > 0:
                return render(request, 'shop/bill_generation.html', {'items': item_query, 'itm': items_json})
            return render(request, 'shop/bill_generation.html', {'message': "No Products to show"})

        elif request.method == 'POST':
            item_query = list(item_query)
            billItems = []
            billTotal = 0

            try:
                # Data from the Request
                data = json.loads(request.body)
                name = data['name']
                request_items = data['items'][0] # Expected: Array
                # Fill the array with Bill Items
                for i in range(len(request_items)):
                    # Array item contains the number of 
                    if request_items[i] != 0:
                        item_total = request_items[i] * item_query[i].price
                        billTotal += item_total
                        currentItem = None

                        # To avoid duplicates, use the same BillItem if already exists
                        item_search = BillItem.objects.filter(item=item_query[i], price=item_query[i].price, 
                                    quantity=request_items[i], total=request_items[i] * item_query[i].price)
                        if item_search.count() != 0:
                            currentItem = item_search[0]
                        else:
                            currentItem = BillItem(item=item_query[i], price=item_query[i].price,
                            quantity=request_items[i], total=request_items[i] * item_query[i].price)
                        # Add to the list
                        billItems.append(currentItem)
                        currentItem.save()

                # Generate Bill and add BillItems from the list
                current_bill = Bill(seller=current_seller, total=billTotal, customer=name, dateTime=now())
                current_bill.save()
                current_bill.items.add(*billItems)
                return JsonResponse({'status': 'Success'})
            except:
                return JsonResponse({'status': 'Server Error'})
        else:
            JsonResponse('Bad Request')
    return render(request, 'shop/bill_generation.html', {'message': "Please Login to View this Page"})


def update_stock(request):
    if request.user.is_authenticated:
        seller = Seller.objects.filter(user=request.user)[0]
        item = Item.objects.filter(seller=seller)
        if item.count() > 0:
            return render(request, 'shop/update_stock.html', {'items': item})
        return render(request, 'shop/update_stock.html', {'message': "No Product to show"})
    return render(request, 'shop/update_stock.html', {'message': "Please Login to View this Page"})


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        if (notifications.count() > 0):
            return render(request, 'shop/notifications.html', {'noti': notifications})
        return render(request, 'shop/notifications.html', {'message': "Nothing to Show"})
    return render(request, 'shop/notifications.html', {'message': "You must be logged in to see this page"})
