from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'email', 'address', 'created', 'updated', 'paid']
    list_filter = ['created', 'updated', 'paid']
    inlines = [OrderItemInLine]


admin.site.register(Order, OrderAdmin)
