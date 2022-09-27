from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

# from ajax_select.admin import AjaxSelectAdmin
# from ajax_select import make_ajax_form
# from django_select2_admin_filters.admin import Select2AdminFilterMixin
# from django_select2_admin_filters.filters import ChoiceSelect2Filter, MultipleChoiceSelect2Filter, ModelSelect2Filter, MultipleModelSelect2Filter

from .models import *
from .forms import *


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
# class MemberProfileAdmin(Select2AdminFilterMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'name',
        'phone_number',
        'birth_date',
        # 'membership_type',
        'date_joined',
        'is_active',
        # 'email_verified',
    ]
    # autocomplete_fields = ['phone_number', ]
    # change_list_template = 'admin/change_list_filter_sidebar.html'
    # list_filter = (
    #     CityFilter,
    # )
    # form = BirthCityAdminForm
    # form = SignUpForm
    # form = make_ajax_form(MemberProfile, {
    #     # fieldname: channel_name
    #     'birth_city': 'birth_city'
    # })

    # def save_model(self, request, obj, form, change):
    #   # import re
    #   import datetime
    #   # display_format = '%d-%m-%Y'
    #   db_format = '%d-%m-%Y'
    #   # db_format = '%Y-%m-%d'
    #   display_format = '%Y-%m-%d'
    #   date = obj.birth_date
    #   date = str(date)
    #   # month, day, year = date.split('-')
    #   # obj.birth_date = '-'.join((day, month, year))
    #   obj.birth_date = datetime.datetime.strptime(date, display_format).strftime(db_format)
    #   # obj.birth_date = str(re.sub('-', '', obj.birth_date))
        # obj.sun_sign = self.full_name
        # super().save_model(request, obj, form, change)


admin.site.register(Profile, ProfileAdmin)
