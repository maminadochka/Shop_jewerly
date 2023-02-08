from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', main_page, name='home'),
    path('catalog', catalog_page, name='product_list'),
    re_path(r'^(?P<category_slug>[-\w]+)/$', catalog_page, name='product_list_by_category'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', product_detail, name='product_detail'),
    path('login', login_page, name='login'),
    path('logout', logout_page, name='logout'),
    path('sign_up', sign_up, name='sign_up'),
]