from django.conf.urls import patterns, include, url

from .views import (
    project_list_view,
    project_summary_view,
    doc_view,
)

urlpatterns = patterns("",
    url(
        r"^$",
        project_list_view,
        name= "project-list"
    ),
    url(
        r"^(?P<project_slug>[\w-]+)/$",
        project_summary_view,
        name= "project-summary"
    ),
    url(
        r"^(?P<project_slug>[\w-]+)/(?P<location>[a-zA-Z0-9_/]+)/$",
        doc_view,
        name= "doc-single"
    ),
)

