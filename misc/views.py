import pytz

from datetime import datetime, date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import (
    SettingsForm,
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
        print (form.cleaned_data["timezone"])

        # Set the timezone in a cookie.
        response.set_cookie(
            key= "timezone",
            value= form.cleaned_data["timezone"],
            # Expire roughly a year from now.
            expires= datetime.now() + timedelta(days= 365)
        )

    return response

