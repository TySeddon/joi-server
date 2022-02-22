from django import template
import json

register = template.Library()

@register.filter
def percentage(value):
    return f"{int(value * 100)}%"

@register.filter
def json_value(value, attr):
    return json.loads(value)[attr]