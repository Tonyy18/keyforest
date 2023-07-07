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
    handle_new_invoice(payment)

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

def finish_new_subscription(inv, sub):
    sub.payment.invoice = inv.invoice
    sub.start_date = inv.start_date
    sub.end_date = inv.end_date
    sub.status = parameters.Stripe.Purchase.Status.paid
    sub.payment.save()
    sub.save()

def handle_new_invoice(inv):
    sub_id = inv.subscription_id
    subs_exist = Purchase.objects.filter(stripe_sub_id=sub_id)
    if(subs_exist.count() == 1):
        sub = subs_exist.first()
        if(sub.status == parameters.Stripe.Purchase.Status.waiting_payment and sub.buyer.id == inv.buyer.id):
            finish_new_subscription(inv, sub)
            return
    
    #New period for existing subscription


def handle_new_subscription(sub):
    purchase = get_purchase_skeleton(sub)
    purchase.stripe_sub_id = sub.subscription_id
    purchase.status = parameters.Stripe.Purchase.Status.waiting_payment
    purchase.payment.save()
    purchase.save()
    #The subscription will be finished when the related invoice comes
    
