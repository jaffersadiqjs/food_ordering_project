from django.shortcuts import render, redirect
from .models import MenuItem
from django.contrib.auth.decorators import login_required

@login_required
def restaurant_dashboard(request):
    items = MenuItem.objects.filter(created_by=request.user)
    return render(request, 'restaurant_dashboard.html', {'items': items})

@login_required
def add_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST.get('description', '')
        MenuItem.objects.create(name=name, price=price, description=description, created_by=request.user)
        return redirect('restaurant_dashboard')
    return render(request, 'add_item.html')
