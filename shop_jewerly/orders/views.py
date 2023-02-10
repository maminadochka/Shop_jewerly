from django.shortcuts import render
from .models import OrderItem
from .forms import OrderForm
from cart.cart import Cart
from .tasks import new_order
from main.models import Product

from django.shortcuts import get_object_or_404

# Create your views here.


def order_create(request):
    cart = Cart(request)

    user = request.user
    user_name = ''
    email = ''

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                product = Product.objects.get(name=item['product'])
                count = product.stock - item['quantity']
                Product.objects.filter(name=item['product']).update(stock=count)
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear_cart()
            new_order.delay(order.id)
            return render(request, 'orders/created_order.html',
                          {'order': order,})
    else:
        form = OrderForm
        if user.is_authenticated:
            user_name = user
            email = request.user.email
    return render(request, 'orders/order_create.html',
                  {'cart': cart, 'user_name': user_name, 'email': email, 'form': form})
