from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def subscription_to_string(license):
    re = parameters.License.duration_types[license.durationType]
    if(license.duration == 1):
        re = re[:-1]
    if(license.durationType > 0):
        re = str(license.duration) + " " + re
    return re