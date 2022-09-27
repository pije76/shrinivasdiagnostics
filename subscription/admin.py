from django.contrib import admin

from .models import *

from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
class PackageAdmin(SummernoteModelAdmin):
    list_display = [
        'id',
        'title',
        'slug',
        'description',
    ]
    # autocomplete_fields = ['ticker_code', ]
    # ModelAdmin.ordering = ('date_price',)
    prepopulated_fields = {'slug': ('title',), }
    summernote_fields = ('description',)


class PackageCostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'subscription',
        'billing_period',
        'billing_unit',
        'price',
    ]
    # autocomplete_fields = ['ticker_code', ]
    # ModelAdmin.ordering = ('date_price',)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'member',
        'subscription',
        # 'ticker',
        # 'indicator',
        'begin_date',
        'expired_date',
        # 'price',
        # 'quantity',
        'active',
        'status',
    ]
    # autocomplete_fields = ['ticker_code', ]
    # ModelAdmin.ordering = ('date_price',)


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageCost, PackageCostAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(TickerCost)
admin.site.register(IndicatorCost)
