from django import template
register = template.Library()
from lib import parameters
from lib.utils import common

@register.simple_tag
def get_purchase_renews_text(purchase):
    p_statuses = parameters.Stripe.Purchase.Status
    b_statuses = parameters.Stripe.Subscription.Status

    if(purchase.subscription == None or 
    purchase.status == p_statuses.expired or
    purchase.subscription.status == b_statuses.cancelled or 
    purchase.subscription.status == b_statuses.expired):
        return "Never"

    return common.format_date(purchase.subscription.end_date, "%d.%m.%Y")

@register.simple_tag
def get_purchase_status_text(purchase):
    res = None
    if(purchase.subscription == None or purchase.subscription.status == parameters.Stripe.Subscription.Status.paid):
        res = parameters.Stripe.Purchase.Status.text[purchase.status]
    else:
        res = parameters.Stripe.Subscription.Status.text[purchase.subscription.status]
    return res.capitalize()

@register.filter
def show_key_button(purchase):
    p_statuses = parameters.Stripe.Purchase.Status
    if(purchase.activated == False and purchase.status == p_statuses.not_activated):
        if(purchase.subscription != None):
            if(purchase.subscription.status == parameters.Stripe.Subscription.Status.paid):
                return True
            return False
        return True
        
    return False
