from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from w0rplib.views import LoginView, LogoutView


def templ(regex, template):
    return (regex, TemplateView.as_view(template_name=template + ".dj.htm"))


admin.autodiscover()

urlpatterns = [
    url(settings.ADMIN_REGEX, admin.site.urls),
    url(settings.LOGIN_REGEX, LoginView.as_view(), name="login"),
    url(settings.LOGOUT_REGEX, LogoutView.as_view()),
    url(r"^blog/", include("blog.urls")),
    url(r"^presentation/", include("presentation.urls")),
    url(
        r"^$",
        RedirectView.as_view(
            url="/blog/",
            permanent=False,
        )
    ),
]

if settings.DEBUG:
    # Serve media files via Django in DEBUG mode.
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    # Serve static files via Django in DEBUG mode.
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
