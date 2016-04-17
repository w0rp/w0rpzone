from django.conf.urls import url

from .views import view_presentation

urlpatterns = [
    url(r"(?P<filename>[a-z0-9\-]+)", view_presentation),
]
