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
        'component',
        'speciment',
        'prerequisites',
        'samplecutoff',
        'available',
        'created',
        'updated',
    ]
    # list_filter=['available','created','updated']
    list_editable=['price','available']
    prepopulated_fields={'slug':('name',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'product',
        'ordered',
        'quantity',
    ]

class CartAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        # 'items',
        'ordered',
        # 'start_date',
        'ordered_date',
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)