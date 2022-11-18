from django.contrib import admin

from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'category',
        'tags',
        'price',
        'discount_price',
        'component',
        'speciment',
        'prerequisites',
        'samplecutoff',
        'available',
        'created',
        'updated',
    ]
    # list_filter=['available','created','updated']
    list_editable=['price', 'discount_price', 'available']
    prepopulated_fields={'slug':('name',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'product',
        'ordered',
        'quantity',
    ]

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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Payment, PaymentAdmin)

