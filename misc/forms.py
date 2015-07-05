import pytz

from django.forms import (
    Form,
    ChoiceField,
)


class SettingsForm (Form):
    timezone = ChoiceField(
        choices=tuple((x, x) for x in pytz.common_timezones),
        label="Time Zone",
        help_text="Set your current time zone here.",
    )
