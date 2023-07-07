from project.models import Checkout_session, Purchase, Payment
from lib.integrations.stripe import stripe_api, stripe_event_objects
from lib.utils import common
from lib import parameters

def payment_succeeded(data):
    payment = stripe_event_objects.Payment(data)
    
def new_subscription(data):
    payment = stripe_event_objects.Subscription(data)
    handle_new_subscription(payment)

def invoice_paid(data):
    payment = stripe_event_objects.Invoice(data)

def get_payment_object(ob):
    pmt = Payment(user=ob.buyer, product=ob.product, price=ob.price)
    if(ob.type == "payment"):
        pmt.receipt = ob.receipt
    
    if(ob.type == "invoice"):
        pmt.invoice = ob.invoice
    return pmt

def get_purchase_skeleton(ob):
    return Purchase(
        buyer=ob.buyer,
        product=ob.product,
        period_id=common.get_random_string(),
        period_tk=1,
        activation_id=common.get_random_string(),
        payment=get_payment_object(ob),
    )

def handle_new_subscription(sub):
    purchase = get_purchase_skeleton(sub)
    purchase.stripe_sub_id = sub.subscription_id
    purchase.status = parameters.Stripe.Purchase.Status.waiting_payment
    purchase.payment.save()
    purchase.save()
    
