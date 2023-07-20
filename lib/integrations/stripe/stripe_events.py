from project.models import Checkout_session, Purchase, Payment, Subscription
from lib.integrations.stripe import stripe_api, stripe_event_objects
from lib.utils import common
from lib import parameters

def payment_succeeded(data):
    payment = stripe_event_objects.Payment(data)
    purchase = get_purchase_skeleton(payment)
    purchase.payment = get_payment_object(payment)
    purchase.payment.save()
    purchase.save()

    
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
        activation_id=common.get_random_string()
    )
def get_subscription_skeleton(ob):
    return Subscription(
        user=ob.buyer,
        product=ob.product,
        stripe_id=ob.subscription_id
    )

def finish_new_subscription(inv, sub):
    #new payment
    payment = get_payment_object(inv)
    payment.invoice = inv.invoice
    #finish the subscription
    sub.payment = payment
    sub.start_date = inv.start_date
    sub.end_date = inv.end_date
    sub.status = parameters.Stripe.Subscription.Status.paid
    sub.payment.save()
    sub.save()
    #new purchase
    purchase = get_purchase_skeleton(inv)
    purchase.subscription = sub
    purchase.save()

def handle_new_invoice(inv):
    sub_id = inv.subscription_id
    subs_exist = Subscription.objects.filter(stripe_id=sub_id)
    if(subs_exist.count() == 1):
        sub = subs_exist.first()
        if(sub.status == parameters.Stripe.Subscription.Status.waiting_payment and sub.user.id == inv.buyer.id):
            finish_new_subscription(inv, sub)
            return
    
    #New period for existing subscription
    latest_row = subs_exist.last()
    prev_period_tk = latest_row.period_tk
    prev_period_id = latest_row.period_id
    
    if(latest_row.status != parameters.Stripe.Purchase.Status.expired):
        #Change previous period to expired
        latest_row.status = parameters.Stripe.Purchase.Status.expired
        latest_row.save()
    #new susbcription
    new_sub = get_subscription_skeleton(inv)
    new_sub.status = parameters.Stripe.Subscription.Status.paid
    new_sub.start_date = inv.start_date
    new_sub.end_date = inv.end_date
    new_sub.period_id = prev_period_id
    new_sub.period_tk = prev_period_tk + 1
    #new payment
    payment = get_payment_object(sub)
    payment.invoice = inv.invoice
    payment.save()
    new_sub.payment = payment
    new_sub.save()
    #update purchase subscription to the new period
    purchase = Purchase.objects.get(subscription=sub)
    purchase.subscription = new_sub
    purchase.save()
    

def handle_new_subscription(sub):
    subscription = get_subscription_skeleton(sub)
    subscription.period_id = common.get_random_string()
    subscription.status = parameters.Stripe.Subscription.Status.waiting_payment
    subscription.save()
    #The subscription will be finished when the related invoice comes
    
