from django import template

register = template.Library()


@register.filter
def first_letters(value):
    if len(value) > 255:
        value = value[:255] + "..."
    return value
