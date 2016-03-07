from django.views.generic.base import RedirectView
from django.conf.urls import url


def redir(regex, redirect_url, name=None):  # pragma: no cover
    """
    A shorter wrapper around RedirectView for 301 redirects.
    """
    return url(
        regex,
        RedirectView.as_view(url=redirect_url, permanent=True),
        name=name,
    )


def redir_temp(regex, redirect_url, name=None):  # pragma: no cover
    """
    A shorter wrapper around RedirectView for 302 redirects.
    """
    return url(
        regex,
        RedirectView.as_view(url=redirect_url, permanent=False),
        name=name,
    )
