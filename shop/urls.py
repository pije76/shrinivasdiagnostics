from django.urls import path, re_path

from .views import *

app_name='shop'

urlpatterns = [
     path('', product_list, name='product_list'),
     # path('', FacetedSearchView.as_view(), name='haystack_search'),
     # re_path(r'^find/', FacetedSearchView.as_view(), name='haystack_search'),
     path('<slug:category_slug>/', product_list, name='product_list_by_category'),
     path('package-description/<int:id>/<slug:slug>/', product_detail, name='product_detail'),
     # re_path(r'^product/(?P<slug>[\w-]+)/$', ProductView.as_view(), name='product'),
     # re_path(r'^search/autocomplete/$', autocomplete),
]