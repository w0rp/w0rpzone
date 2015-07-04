import html

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def word_break_on(value, split_value):
    """
    Given a string and a substring to split the string on, return
    a string as safe HTML with word break opportunities set on the splits.
    """
    split_value = html.escape(split_value)

    return mark_safe(
        (split_value + "<wbr>").join(
            html.escape(x)
            for x in
            value.split(split_value)
        )
    )
