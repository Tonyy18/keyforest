from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def subscription_to_string(license):
    re = parameters.License.Subscription_period_type.text[license.subscription_type]
    if(license.subscription_period == 1):
        re = re[:-1]
    if(license.subscription_type > 0):
        re = str(license.subscription_period) + " " + re
    return re

@register.simple_tag
def subscription_to_readable(license):
    if(license.subscription_period == 1 or license.subscription_type == 0):
        return parameters.License.Subscription_period_type.singular_text[license.subscription_type].capitalize()
    return "Every " + str(license.subscription_period) + " " + parameters.License.Subscription_period_type.text[license.subscription_type]