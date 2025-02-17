from django import template

register = template.Library()

@register.filter
def model_name(object):
    try:
        return object._meta.model_name
    except AttributeError:
        return None