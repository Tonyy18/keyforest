from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def get_purchase_renews_text(purchase):
    return purchase.get_next_invoice_status()

@register.simple_tag
def get_purchase_status_text(purchase):
    return purchase.get_status()

@register.filter
def show_key_button(purchase):
    return purchase.is_activable()

@register.simple_tag
def get_invoice_status_text(invoice):
    return parameters.Stripe.Invoice.Status.text[invoice.status].capitalize()

@register.filter
def show_invoice_button(invoice):
    return invoice.invoice != None and invoice.status != parameters.Stripe.Invoice.Status.void

@register.filter
def show_cancel_button(purchase):
    return purchase.is_cancellable()