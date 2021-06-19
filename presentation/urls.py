from django.conf.urls import re_path

from .views import view_presentation

urlpatterns = [
    re_path(r"(?P<filename>[a-z0-9\-]+)", view_presentation),
]
