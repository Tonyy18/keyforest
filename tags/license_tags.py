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

@register.simple_tag
def subscription_to_readable(license):
    if(license.subscription_period == 1 or license.subscription_type == 0):
        return parameters.License.subscription_types_simple[license.subscription_type].capitalize()
    return "Every " + str(license.subscription_period) + " " + parameters.License.subscription_types[license.subscription_type]

@register.simple_tag
def number_to_price(num):
    price = str(num)
    re = None
    if("." not in price):
        re = price + ".00"
    else:
        sp = price.split(".")
        if(len(sp[1]) < 2):
            re = price + "0"
        else:
            re = price
    return re + "$"