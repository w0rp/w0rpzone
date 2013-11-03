from django.conf.urls import patterns, include, url
from django.contrib import admin

import settings

admin.autodiscover()

urlpatterns = patterns("",
    url(settings.ADMIN_REGEX, include(admin.site.urls)),
    # Include all of the blog app urls.
    url(r"^blog/", include("blog.urls")),
)
