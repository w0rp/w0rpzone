import pytz

from w0rplib.form import Form

from django.forms import (
    ChoiceField,
)


class SettingsForm (Form):
    timezone = ChoiceField(
        choices=tuple((x, x) for x in pytz.common_timezones),
        label="Time Zone",
        help_text="Set your current time zone here.",
    )
