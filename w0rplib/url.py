from django.views.generic.base import RedirectView
from django.conf.urls import re_path


def redir(regex, redirect_url, name=None):
    """
    A shorter wrapper around RedirectView for 301 redirects.
    """
    return re_path(
        regex,
        RedirectView.as_view(url=redirect_url, permanent=True),
        name=name,
    )


def redir_temp(regex, redirect_url, name=None):
    """
    A shorter wrapper around RedirectView for 302 redirects.
    """
    return re_path(
        regex,
        RedirectView.as_view(url=redirect_url, permanent=False),
        name=name,
    )
