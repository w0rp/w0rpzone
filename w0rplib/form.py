import django.forms


class ConvenientFormMixin:
    # This method is implemented in the next Django version, and can be removed
    # after the next version is stable.
    def add_error(self, field_name, error_message):
        self.errors.setdefault(
            field_name,
            self.error_class()
        ).append(error_message)

        if field_name in self.cleaned_data:
            del self.cleaned_data[field_name]


class Form(ConvenientFormMixin, django.forms.Form):
    error_css_class = "error"


class ModelForm(ConvenientFormMixin, django.forms.ModelForm):
    error_css_class = "error"
