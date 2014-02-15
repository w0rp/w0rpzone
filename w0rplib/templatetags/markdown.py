import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from w0rplib.decorator import print_return_value

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(markdown2.markdown(
        text= value,
        extras= ["fenced-code-blocks", "code-friendly"],
        safe_mode= True,
    ))

# Not really safe, but Django needs to think it is.
@register.filter(is_safe=True)
@stringfilter
def unsafe_markdown(value):
    return mark_safe(markdown2.markdown(
        text= value,
        extras= [
            "fenced-code-blocks",
            "code-friendly"
            # Website authors using full markdown have more power.
            "footnotes",
            "wiki-tables",
            "header-ids",
        ],
    ))

