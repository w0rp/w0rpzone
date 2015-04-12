# This settings file contains most of the settings needed for a dev machine.

from settings_base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PIPELINE_ENABLED = False

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ("127.0.0.1",)
MANAGERS = ADMINS = ()

SECRET_KEY = "thisisntverysecretnowisit?"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
