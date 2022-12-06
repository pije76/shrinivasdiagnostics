from django.urls import path, re_path

from .views import *

app_name='shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('add-to-cart/<pk>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove_from_cart'),
	path('reduce-quantity-item/<pk>/', reduce_quantity_item, name='reduce_quantity_item'),
    # path("callback/", callback, name="callback"),
    # path('order-summary/', order_summary, name='order_summary'),
    # path('order/', order, name='order'),
    # path('payment/<payment_option>/', payment, name='payment'),
    # path('paymenthandler/', paymenthandler, name='paymenthandler'),
    # path('', FacetedSearchView.as_view(), name='haystack_search'),
    # path('find/', FacetedSearchView.as_view(), name='haystack_search'),
    # path('product/(?P<slug>[\w-]+)/$', ProductView.as_view(), name='product'),
    # path('search/autocomplete/$', autocomplete),
]
