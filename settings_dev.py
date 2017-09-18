# This settings file contains most of the settings needed for a dev machine.

from settings_base import *  # noqa

DEBUG = True
PIPELINE["PIPELINE_ENABLED"] = False  # noqa

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ("127.0.0.1",)
MANAGERS = ADMINS = (
    ("w0rp", "devw0rp@gmail.com"),
)

SECRET_KEY = "thisisntverysecretnowisit?"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
