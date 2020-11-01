from django.shortcuts import render
from .models import Item
# Create your views here.
def home(request):
    return render(request, 'shop/index.html')

def dashboard(request):
    items = Item.objects.order_by('name')
    print(items)
    return render(request, 'shop/Item_Available.html',{'items': items})
    
def notifications(request):
    return render(request, 'shop/notifications.html')

def Item_Available(request):
    #sellers = Seller.objects.filter(user = request.user)
    #for i in range(10):
    #    nam = f'Item {i}'
    #    Item(name = nam, price=  10, size= '500ml',quantity_available= 50,min_quantity=i+10, seller = sel).save()

    return render(request, 'shop/Item_Available.html')