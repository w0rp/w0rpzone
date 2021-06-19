from django.conf import settings
from django.conf.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView

from w0rplib.views import LoginView, LogoutView


def templ(regex, template):
    return (regex, TemplateView.as_view(template_name=template + ".dj.htm"))


admin.autodiscover()

urlpatterns = [
    re_path(settings.ADMIN_REGEX, admin.site.urls),
    re_path(settings.LOGIN_REGEX, LoginView.as_view(), name="login"),
    re_path(settings.LOGOUT_REGEX, LogoutView.as_view()),
    re_path(r"^blog/", include("blog.urls")),
    re_path(r"^presentation/", include("presentation.urls")),
    re_path(
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
