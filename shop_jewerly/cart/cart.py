from decimal import Decimal
from main.models import Product
from django.conf import settings
from django.shortcuts import get_object_or_404


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save_changes(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add_to_cart(self, product, quantity=1, update=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save_changes()

    def delete_from_cart(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save_changes()

    def get_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear_cart(self):
        #del self.session[settings.CART_SESSION_ID]
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
        self.save_changes()

    def __iter__(self):
        product_ids = self.cart.keys()

        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
           # product_id = product.id

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())




