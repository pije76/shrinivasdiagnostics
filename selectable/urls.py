from django.urls import include, re_path

from . import views


urlpatterns = [
    re_path(r'^(?P<lookup_name>[-\w]+)/$', views.get_lookup, name="selectable-lookup"),
]
