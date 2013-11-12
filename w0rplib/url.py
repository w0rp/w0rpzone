from django.views.generic.base import RedirectView

def redir(regex, url):
    """
    A shorter wrapper around RedirectView.
    """
    return (regex, RedirectView.as_view(url= url))

