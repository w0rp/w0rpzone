from django.conf.urls import patterns, include, url

from .views import (
    doc_view,
)

urlpatterns = patterns("",
    url(
        r"^(?P<project_slug>[\w-]+)/(?P<location>[a-zA-Z0-9_/]+)/$",
        doc_view,
        name= "doc-single"
    ),
)

