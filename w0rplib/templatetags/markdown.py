from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import bleach
import markdown2

register = template.Library()


# Not really safe, but Django needs to think it is.
@register.filter(is_safe=True)
@stringfilter
def unsafe_markdown(value):
    return mark_safe(markdown2.markdown(
        text=value,
        extras=[
            "fenced-code-blocks",
            "code-friendly",
            "highlightjs-lang",
        ],
    ))


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    html = unsafe_markdown(value)

    return bleach.clean(
        html,
        tags=[
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'code',
            'em',
            'i',
            'li',
            'ol',
            'p',
            'pre',
            'strong',
            'ul',
        ],
        attributes={
            'a': ['href', 'title'],
            'abbr': ['title'],
            'acroynym': ['title'],
            'code': ['class'],
        },
        protocols=[
            'http',
            'https',
            'mailto',
        ],
    )
