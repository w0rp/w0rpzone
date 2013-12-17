from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import (
    login as login_view,
    logout as logout_view
)
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic import RedirectView

def templ(regex, template):
    return (regex, TemplateView.as_view(template_name= template + ".dj.htm"))

admin.autodiscover()

urlpatterns = patterns("",
    (settings.ADMIN_REGEX, include(admin.site.urls)),
    url(settings.LOGIN_REGEX, login_view, {
        "template_name": "registration/login.dj.htm",
    }),
    url(settings.LOGOUT_REGEX, logout_view, {
        "next_page": settings.LOGOUT_REDIRECT_URL,
    }),
    # Include all of the blog app urls.
    (r"^blog/", include("blog.urls")),
    # Include all of the hording urls.
    (r"^hording/", include("hording.urls")),
)

urlpatterns += patterns("",
    # TODO: Implement a more meaningful homepage.
    # templ(r"^$", "index"),
    (r"^$", RedirectView.as_view(
        url= "/blog/",
        permanent= False,
    )),
)

if settings.DEBUG:
    # Serve media files via Django in DEBUG mode.
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)

    # Serve static files via Django in DEBUG mode.
    urlpatterns += static(settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)

