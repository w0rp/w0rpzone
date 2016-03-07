from django.http import HttpResponse
from django.utils import timezone
from django.views.generic.edit import FormMixin, FormView
from django.core.urlresolvers import reverse_lazy

import datetime

from .forms import SettingsForm


class JSONFormMixin(FormMixin):
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.is_ajax():
            return HttpResponse(
                "{}",
                content_type="application/json",
                status=200,
            )

        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)

        if self.request.is_ajax():
            return HttpResponse(
                form.errors.as_json(),
                content_type="application/json",
                status=400,
            )

        return response


class JSONFormView(JSONFormMixin, FormView):
    pass


class SettingsView(JSONFormView):
    form_class = SettingsForm
    template_name = "settings.dj.htm"
    success_url = reverse_lazy("settings")

    def get_initial(self):
        return {
            "timezone": timezone.get_current_timezone_name()
        }

    def form_valid(self, form):
        # Activate the new timezone first before rendering the template.
        timezone.activate(form.cleaned_data["timezone"])

        response = super().form_valid(form)

        # Set the timezone in a cookie.
        response.set_cookie(
            key="timezone",
            value=form.cleaned_data["timezone"].zone,
            # Expire roughly a year from now.
            expires=timezone.now() + datetime.timedelta(days=365)
        )

        return response
