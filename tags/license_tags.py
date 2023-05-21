from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def subscription_to_string(license):
    re = parameters.License.subscription_types[license.subscription_type]
    if(license.subscription_period == 1):
        re = re[:-1]
    if(license.subscription_type > 0):
        re = str(license.subscription_period) + " " + re
    return re