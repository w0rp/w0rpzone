import pytz
from pytz.exceptions import UnknownTimeZoneError

from datetime import datetime, date, timedelta

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from w0rplib.view import json_view, json_response, ClientError

from .forms import (
    SettingsForm,
)

def set_timezone_cookie(response, timezone_string):
    response.set_cookie(
        key= "timezone",
        value= timezone_string,
        # Expire roughly a year from now.
        expires= datetime.now() + timedelta(days= 365)
    )

def settings_view(request):
    form = SettingsForm(
        request.POST or None,
        initial= {
            "timezone": timezone.get_current_timezone_name()
        }
    )

    if form.is_valid() and request.method == "POST":
        # Activate the new timezone first before rendering the template.
        timezone.activate(pytz.timezone(form.cleaned_data["timezone"]))

    response = render(request, "settings.dj.htm", {
        "form": form,
    })

    if form.is_valid() and request.method == "POST":
        # Set the timezone in a cookie.
        set_timezone_cookie(response, form.cleaned_data["timezone"])

    return response

@csrf_exempt
@json_view
@require_POST
def ajax_settings_view(request):
    timezone_string = request.POST.get("timezone")

    if timezone_string:
        # Assert on the timezone.
        try:
            pytz.timezone(timezone_string)
        except UnknownTimeZoneError:
            raise ClientError("Invalid timezone!")

    response = json_response({})

    if timezone_string:
        set_timezone_cookie(response, timezone_string)

    return response

