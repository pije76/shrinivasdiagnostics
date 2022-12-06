from django.contrib import admin

from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','slug']
    prepopulated_fields={'slug':('title',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
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
    list_editable = [
        'title',
        'slug',
        'category',
        'tags',
        'price',
        'discount_price',
        'available',
        'speciment',
        'prerequisites',
        'samplecutoff',
        'available',
    ]
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
