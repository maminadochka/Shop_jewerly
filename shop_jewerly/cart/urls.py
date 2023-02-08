from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path('add/<int:product_id>/', add_product_to_cart, name='add_product_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('', cart_detail, name='cart_detail'),
]

