from django import template
register = template.Library()
from lib import parameters
from lib.utils import common

@register.simple_tag
def get_purchase_renews_text(purchase):
    return "test"

@register.simple_tag
def get_purchase_status_text(purchase):
    return "test"

@register.filter
def show_key_button(purchase):
    return True

@register.simple_tag
def get_invoice_status_text(invoice):
    return parameters.Stripe.Invoice.Status.text[invoice.status].capitalize()
