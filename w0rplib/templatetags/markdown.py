import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from w0rplib.decorator import print_return_value

register = template.Library()

def fix_spaces(markdown):
    """
    Fix spaces in generated markdown by replacing them with
    non-breaking spaces.
    """
    def generate_characters():
        in_tag = False

        for char in markdown:
            if not in_tag and char == " ":
                yield "&nbsp;"
                continue

            if in_tag and char == ">":
                in_tag = False
            elif not in_tag and char == "<":
                in_tag = True

            yield char

    return "".join(generate_characters())

@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(fix_spaces(markdown2.markdown(
        text= value,
        extras= ["fenced-code-blocks", "code-friendly"],
        safe_mode= True,
        enable_attributes= False,
    )))

# Not really safe, but Django needs to think it is.
@register.filter(is_safe=True)
@stringfilter
def unsafe_markdown(value):
    return mark_safe(fix_spaces(markdown2.markdown(
        text= value,
        extras= [
            "fenced-code-blocks",
            "code-friendly"
            # Website authors using full markdown have more power.
            "footnotes",
            "wiki-tables",
            "header-ids",
        ],
    )))

