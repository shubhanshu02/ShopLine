from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Notification, Seller, Item, BillItem, Bill
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils import datetime_safe
# Create your views here.


def home(request):
    return render(request, 'shop/index.html')


@login_required
def stock(request):
    seller = Seller.objects.filter(user=request.user)[0]
    item = Item.objects.filter(seller=seller)
    if item.count() > 0:
        return render(request, 'shop/item_Available.html', {'items': item})
    return render(request, 'shop/item_Available.html', {'message': "No Product to show"})


@login_required
def dashboard(request):
    seller = Seller.objects.filter(user=request.user)[0]
    old_bills = Bill.objects.filter(seller=seller)
    return render(request, 'shop/dashboard_home.html', {'seller': seller, 'old_bills': old_bills})


@csrf_exempt
@login_required
def bill_generate(request):
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
            request_items = data['items'][0]  # Expected: Array
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
                    item_query[i].quantity_available -= request_items[i]
                    # Generate notification if quantity becomes less
                    if item_query[i].quantity_available < item_query[i].min_quantity:
                        Notification(user=current_seller,
                                     item=item_query[i], date=now()).save()
                    # Add to the list
                    billItems.append(currentItem)
                    item_query[i].save()
                    currentItem.save()
            # Generate Bill and add BillItems from the list
            current_bill = Bill(
                seller=current_seller, total=billTotal, customer=name, dateTime=now())
            current_bill.save()
            current_bill.items.add(*billItems)
            return JsonResponse({'status': 'Success'})
        except:
            return JsonResponse({'status': 'Server Error'})
    else:
        return JsonResponse({'status': 'Bad Request'})


@csrf_exempt
@login_required
def update_stock(request):
    current_seller = Seller.objects.get(user=request.user)
    item_query = Item.objects.filter(seller=current_seller)
    if request.method == "GET":
        items_json = item_query.values_list()
        items_json = json.dumps(list(items_json), cls=DjangoJSONEncoder)
        if item_query.count() > 0:
            return render(request, 'shop/update_stock.html', {'items': item_query, 'itm': items_json})
        return render(request, 'shop/update_stock.html', {'message': "No Product to show"})
    elif request.method == 'POST':
        try:
            name = request.POST.get('name')
            size = request.POST.get('size')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            min_qty = request.POST.get('min')
        except Exception as exc:
            return JsonResponse({'status': str(exc)})
        try:
            item = Item.objects.get(name=name, seller=current_seller)
            item.size = size
            item.price = price
            item.quantity_available = quantity
            item.min_quantity = min_qty
            item.save()
        except Exception as exc:
            return JsonResponse({'status': str(exc)})

        return JsonResponse({'status': 'Success'})
    else:
        JsonResponse({'status': 'Bad Request'})


@login_required
def notifications(request):
    seller = Seller.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=seller)
    if (notifications.count() > 0):
        return render(request, 'shop/notifications.html', {'noti': notifications})
    return render(request, 'shop/notifications.html', {'message': "Nothing to Show"})


@csrf_exempt
@require_POST
def newItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Bad Request'})
    try:
        current_seller = Seller.objects.get(user=request.user)
        name = request.POST.get('name')
        size = request.POST.get('size')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        min_qty = request.POST.get('min')
    except Exception as exc:
        return JsonResponse({'status': str(exc)})
    try:
        item = Item.objects.create(
            name=name, size=size, price=price, quantity_available=quantity, min_quantity=min_qty, seller=current_seller)
        item.save()
    except IntegrityError:
        return JsonResponse({'status': "An Item with Same Name Already Exists"})
    return JsonResponse({'status': 'Success'})


@csrf_exempt
@require_POST
def deleteItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Bad Request'})
    try:
        current_seller = Seller.objects.get(user=request.user)
        name = request.POST.get('name')
        item = Item.objects.get(name=name)
        item.delete()
    except Exception as exc:
        return JsonResponse({'status': str(exc)})
    return JsonResponse({'status': 'Success'})
