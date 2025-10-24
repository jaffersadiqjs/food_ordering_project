from django.shortcuts import render, redirect
from restaurant.models import MenuItem
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def menu(request):
    items = MenuItem.objects.filter(is_available=True)
    return render(request, 'menu.html', {'items': items})

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[item_id] = cart.get(item_id, 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for item_id, qty in cart.items():
        item = MenuItem.objects.get(id=item_id)
        subtotal = item.price * qty
        total += subtotal
        items.append({'item': item, 'qty': qty, 'subtotal': subtotal})
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        total = sum(MenuItem.objects.get(id=i).price * q for i, q in cart.items())
        order = Order.objects.create(user=request.user, total_amount=total)
        for item_id, qty in cart.items():
            item = MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=qty)
        request.session['cart'] = {}
        return redirect('order_success')
    return render(request, 'checkout.html')

def order_success(request):
    return render(request, 'order_success.html')
