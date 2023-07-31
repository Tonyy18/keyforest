from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def get_subscription_types():
    return str(parameters.License.Subscription_period_type.text).replace("'", "\"")

@register.simple_tag
def get_checkout_page_desc_break_length():
    return parameters.Pages.Checkout.desc_hide_length