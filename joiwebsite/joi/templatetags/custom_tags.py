from django import template
import json

register = template.Library()

@register.filter
def percentage(value):
    if value:
        return f"{int(value * 100)}%"
    else:
        return "Error"        

@register.filter
def json_value(value, attr):
    try:
        if type(value).__name__ == "dict":
            return value[attr]
        else:
            return json.loads(value)[attr]
    except:
        return None            