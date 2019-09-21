from django import template
from django.template.defaultfilters import stringfilter

import readtime

register = template.Library()


@register.filter()
@stringfilter
def reading_time(value):
    return readtime.of_markdown(value)
