from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login as login_view
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

def templ(regex, template):
    return (regex, TemplateView.as_view(template_name= template + ".dj.htm"))

admin.autodiscover()

urlpatterns = patterns("",
    (settings.ADMIN_REGEX, include(admin.site.urls)),
    url(settings.LOGIN_REGEX, login_view, {
        "template_name": "registration/login.dj.htm",
    }),
    # Include all of the blog app urls.
    (r"^blog/", include("blog.urls")),
    # Include all of the hording urls.
    (r"^hording/", include("hording.urls")),
)

urlpatterns += patterns("",
    templ(r"^$", "index"),
)

if settings.DEBUG:
    # Serve media files via Django in DEBUG mode.
    urlpatterns += patterns("",
        url(r"^media/(?P<path>.*)$", "django.views.static.serve", {
            "document_root": settings.MEDIA_ROOT
        }),
    )

    # Serve static files via Django in DEBUG mode.
    urlpatterns += static(settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)

