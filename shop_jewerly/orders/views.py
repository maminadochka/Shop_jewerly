from django.shortcuts import render
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderForm
from cart.cart import Cart
from .tasks import new_order
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear_cart()
            new_order.delay(order.id)
            return render(request, 'orders/created_order.html',
                          {'order': order})
    else:
        form = OrderForm
    return render(request, 'orders/order_create.html',
                  {'cart': cart, 'form': form})
