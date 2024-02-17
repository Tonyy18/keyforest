from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def get_null_placeholder(value):
    if(value == None):
        return "-"
    return value

@register.simple_tag
def booleans_to_text(value):
    if(value == True):
        return "Yes"
    return "No"