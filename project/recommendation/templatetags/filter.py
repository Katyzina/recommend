from django import template

register = template.Library()


@register.filter
def first_letters(value):
    if len(value) > 255:
        value = value[:255] + "..."
    return value


@register.filter
def name_of_resume(value:str):
    parts = value.split("/")
    name = parts[-1].split("_")[-1]
    return name
