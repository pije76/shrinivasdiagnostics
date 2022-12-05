from django.contrib import admin

from .models import *

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
# class MemberProfileAdmin(Select2AdminFilterMixin, admin.ModelAdmin):
    list_display = [
        'user',
        'address',
        'state',
        'city',
        'country',
        'location',
        'pin_code',
        'zip',
    ]

admin.site.register(Address, AddressAdmin)
