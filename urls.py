from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns("",
    url(settings.ADMIN_REGEX, include(admin.site.urls)),
    # Include all of the blog app urls.
    url(r"^blog/", include("blog.urls")),
)

if settings.DEBUG:
    # Serve media files via Django in DEBUG mode.
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        }),
    )

    # Serve static files via Django in DEBUG mode.
    urlpatterns += static(settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)

