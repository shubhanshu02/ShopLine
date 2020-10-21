from django.shortcuts import render
from .models import Seller
# Create your views here.
def post_list(request):
    posts = Seller.objects.all()
    return render(request, 'shop/post_list.html', {'posts': posts})