from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *

# Register your models here.
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        # 'user',
        'full_name',
        'phone_number',
        'city',
    ]

admin.site.register(Schedule, ScheduleAdmin)
