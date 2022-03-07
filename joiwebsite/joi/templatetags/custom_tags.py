from django import template
import json

register = template.Library()

@register.filter
def percentage(value):
    if value is not None:
        try:
            return f"{int(float(value) * 100)}%"
        except:
            pass            
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