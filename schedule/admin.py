from django.contrib import admin

from .models import *

# Register your models here.
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'phone_number',
        'city',
    ]

admin.site.register(Schedule, ScheduleAdmin)
