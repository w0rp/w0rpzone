import pytz

from django.utils import timezone

class LocaleMiddleware:
    def process_request(self, request):
        timezone_name = request.COOKIES.get("timezone")

        if timezone_name:
            timezone.activate(pytz.timezone(timezone_name))
        else:
            timezone.deactivate()

