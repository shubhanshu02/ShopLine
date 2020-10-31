from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'shop/index.html')

def dashboard(request):
    return render(request, 'shop/dashboard.html')
    
def notifications(request):
    return render(request, 'shop/notifications.html')