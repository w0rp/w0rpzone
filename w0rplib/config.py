import datetime

import pytz

from django.apps import AppConfig


class Config(AppConfig):
    name = "w0rplib"
    label = "w0rplib"

    def ready(self):
        from . import middleware

        # Set the startup time in the middleware when the app starts.
        middleware.startup_time = datetime.datetime.now(pytz.utc)
