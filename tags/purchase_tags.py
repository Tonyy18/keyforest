from django import template
register = template.Library()
from lib import parameters
from lib.utils import common

@register.simple_tag
def get_purchase_renews_text(purchase):
    text = ""
    if(purchase.product.subscription_type == 0 or purchase.subscription.status != parameters.Stripe.Subscription.Status.active):
        text = "Not invoicing"
    else:
        text = common.format_date(purchase.subscription.end_date)
    return text

@register.simple_tag
def get_purchase_status_text(purchase):
    status = ""
    if(purchase.product.subscription_type == 0 or purchase.subscription.status == parameters.Stripe.Subscription.Status.active):
        status = parameters.Stripe.Purchase.Status.text[purchase.status]
    else:
        #subscription
        status = parameters.Stripe.Subscription.Status.text[purchase.subscription.status]
    return status.capitalize()

@register.filter
def show_key_button(purchase):
    return True

@register.simple_tag
def get_invoice_status_text(invoice):
    return parameters.Stripe.Invoice.Status.text[invoice.status].capitalize()

@register.filter
def show_invoice_button(invoice):
    return invoice.invoice != None and invoice.status != parameters.Stripe.Invoice.Status.void
