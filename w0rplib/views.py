from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView


class LoginView(DjangoLoginView):
    template_name = 'registration/login.dj.htm'


class LogoutView(DjangoLogoutView):
    pass
