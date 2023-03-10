from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import CartForm
from .cart import Cart
from main.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@require_POST
def add_product_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        available_count = data['quantity']
        if available_count <= product.stock:
            cart.add_to_cart(product=product,
                             quantity=data['quantity'],
                             update=data['update'])
            return redirect('cart:cart_detail')
        else:
            messages.error(request, 'Sorry, this jewelry is not available in this quantity.')
    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.delete_from_cart(product)
    return redirect('cart:cart_detail')


#the cart status
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartForm(initial={'quantity': item['quantity'],
                                                         'update': True})
    return render(request, 'cart/details.html', {'cart': cart})
