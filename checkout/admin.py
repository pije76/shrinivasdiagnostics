from django.contrib import admin

from .models import *

# Register your models here.
class CheckoutAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        # 'items',
        'ordered',
        # 'start_date',
        'ordered_date',
    ]

class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'status',
        'razorpay_order_id',
        'payment_id',
        'signature_id',
    ]


admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Payment, PaymentAdmin)
