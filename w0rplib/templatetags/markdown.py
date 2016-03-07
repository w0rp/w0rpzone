import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(markdown2.markdown(
        text=value,
        extras=["fenced-code-blocks", "code-friendly"],
        safe_mode="escape",
    ))


# Not really safe, but Django needs to think it is.
@register.filter(is_safe=True)
@stringfilter
def unsafe_markdown(value):
    return mark_safe(markdown2.markdown(
        text=value,
        extras=["fenced-code-blocks", "code-friendly"],
    ))
