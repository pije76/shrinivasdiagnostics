"""shrinivasdiagnostics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from shop.views import *
from order.views import *


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('profile/', include('accounts.urls')),
    path('book-blood-test-online-in-india/', include('shop.urls')),
    path('package-description/<pk>/', product_detail, name='product_detail'),
    path('shopping-cart/', shopping_cart, name='shopping_cart'),
    path('checkout/', checkout, name='checkout'),
    path("callback/", callback, name="callback"),
	# path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path("payment/", order_payment, name="order_payment"),
    path('my-orders/', my_orders, name='my_orders'),

    path('summernote/', include('django_summernote.urls')),
    path('selectable/', include('selectable.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
