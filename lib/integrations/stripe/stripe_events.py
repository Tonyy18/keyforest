from project.models import Checkout_session, Purchase, Payment
from lib.integrations.stripe import stripe_api, stripe_event_objects
from lib.utils import common

def payment_succeeded(data):
    payment = stripe_event_objects.Payment(data)
    
def new_subscription(data):
    payment = stripe_event_objects.Subscription(data)
    handle_new_subscription(payment)

def invoice_paid(data):
    payment = stripe_event_objects.Invoice(data)

def get_payment_object(ob):
    pmt = Payment(user=ob.buyer, product=paymeobnt.product, price=ob.price)
    if(ob.type == "payment"):
        pmt.receipt = ob.receipt
    
    if(ob.type == "invoice"):
        pmt.invoice = ob.invoice
    return pmt

def get_purchase_skeleton(ob):
    return Purchase(buyer=ob.buyer, product=ob.product)

def handle_new_subscription(sub):
    pmt = get_payment_object(sub)
    pmt.save()
    
    purchase = Purchase(buyer=sub.buyer, product=sub.product)
