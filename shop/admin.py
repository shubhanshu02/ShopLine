from django.contrib import admin
from .models import Seller, Item, BillItem, Bill

admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(BillItem)
admin.site.register(Bill)
