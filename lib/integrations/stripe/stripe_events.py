from project.models import Checkout_session, Purchase, Payment, Subscription, Invoice
from lib.integrations.stripe import stripe_api, stripe_event_objects, stripe_invoices
from lib.utils import common
from lib import parameters

def payment_succeeded(data):
    payment = stripe_event_objects.Payment(data)
    purchase = get_purchase_skeleton(payment)
    purchase.payment = get_payment_object(payment)
    purchase.payment.save()
    purchase.save()

def new_subscription(data):
    sub_ob = stripe_event_objects.Subscription(data)
    sub = get_subscription_skeleton(sub_ob)
    inv = Invoice.objects.filter(subscription_stripe_id = sub_ob.subscription_id)
    if(len(inv) > 1):
        raise Exception("There was multiple invoices created before subscription creation")
    if(len(inv) == 1):
        sub.invoice = inv[0]

    purchase = get_purchase_skeleton(sub_ob)
    purchase.subscription = sub
    sub.save()
    purchase.save()

def update_subscription(data):
    sub_ob = stripe_event_objects.Subscription(data)
    try:
        sub = Subscription.objects.get(stripe_id=sub_ob.subscription_id)
    except:
        raise Exception("Subscription not found for update with id: " + sub_ob.subscription_id)

    sub.status = getattr(parameters.Stripe.Subscription.Status,sub_ob.status)
    sub.start_date = sub_ob.start_date
    sub.end_date = sub_ob.end_date
    sub.save()

def new_invoice(data):
    inv_ob = stripe_event_objects.Invoice(data)
    print(data)
    inv = get_invoice_skeleton(inv_ob)
    existing = Invoice.objects.filter(subscription_stripe_id=inv_ob.subscription_id)
    if(len(existing) > 0):
        prev_tk = existing.last().tk
        inv.tk = prev_tk + 1
    inv.save()
    sub = Subscription.objects.filter(stripe_id = inv_ob.subscription_id)
    if(len(sub) > 0):
        sub = sub.last()
        sub.invoice = inv
        sub.save()

def update_invoice(data):
    inv_ob = stripe_event_objects.Invoice(data)
    invoice = Invoice.objects.get(stripe_id = inv_ob.id)
    invoice.status = getattr(parameters.Stripe.Invoice.Status, inv_ob.status)
    if(invoice.invoice == None):
        invoice.invoice = inv_ob.invoice
    invoice.save()

def get_payment_object(ob):
    pmt = Payment(user=ob.buyer, product=ob.product, price=ob.price, date=ob.created)
    pmt.receipt = ob.receipt
    return pmt

def get_invoice_skeleton(ob):
    return Invoice(
        user=ob.buyer,
        product=ob.product,
        stripe_id=ob.id,
        price=ob.price,
        date=ob.created,
        subscription_stripe_id=ob.subscription_id,
        status = getattr(parameters.Stripe.Invoice.Status, ob.status),
        invoice=ob.invoice
    )

def get_purchase_skeleton(ob):
    return Purchase(
        user=ob.buyer,
        product=ob.product,
        activation_id=common.get_random_string(length=30)
    )
def get_subscription_skeleton(ob):
    return Subscription(
        user=ob.buyer,
        product=ob.product,
        stripe_id=ob.subscription_id,
        status=getattr(parameters.Stripe.Subscription.Status, ob.status),
        start_date=ob.start_date,
        end_date=ob.end_date
    )

def subscription_deleted(data):
    try:
        sub_object = stripe_event_objects.Subscription(data)
        subs = Subscription.objects.filter(stripe_id=sub_object.subscription_id)
        current_period = subs.last()
        current_period.status = parameters.Stripe.Subscription.Status.cancelled
        current_period.save()
    except:
        raise Exception("Failed to change subscription status when subscription cancelled: subscription id: " + sub_object.subscription_id)

    try:
        purchase = Purchase.objects.get(subscription=current_period)
        purchase.status = parameters.Stripe.Purchase.Status.expired
        purchase.save()
    except:
        raise Exception("Failed to change purchase status when subscription cancelled: subscription id: " + sub_object.subscription_id)

    
