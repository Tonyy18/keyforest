from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def get_thumbnail_name(name):
    if(len(name) > parameters.Application.thumbnail_name_length):
        return name[0:parameters.Application.thumbnail_name_length] + "..."
    return name