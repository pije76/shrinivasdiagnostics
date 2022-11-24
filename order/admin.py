from django.contrib import admin

from .models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'item_order',
        'product',
        'quantity',
        'order_date',
    ]


class CheckoutAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered',
        'payment_id',
        'provider_order_id',
        'signature_id',
        'status',
        'amount',
        'checkout_date',
        'billing_address',
    ]

    filter_horizontal = ['items']


admin.site.register(Order, OrderAdmin)
admin.site.register(Checkout, CheckoutAdmin)
