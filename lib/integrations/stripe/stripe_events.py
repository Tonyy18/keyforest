from project.models import Purchase, Payment, Subscription, Invoice, Transaction, Stripe_account
from lib.integrations.stripe import stripe_api, stripe_event_objects, stripe_invoices, stripe_connect
from lib.utils import common
from lib import parameters
from lib.utils import transactions, api_utils
from project.models import Stripe_account

def payment_succeeded(data):
    payment = stripe_event_objects.Payment(data)
    purchase = get_purchase_skeleton(payment)
    pm = get_payment_object(payment)
    tr = get_transaction_skeleton(payment)
    tr.save()
    transactions.add_related(tr, payment)
    transactions.update_product_revenues(tr)
    pm.transaction = tr
    pm.save()
    purchase.payment = pm
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

def update_subscription(data, status=None, current_invoice_status=None):
    sub_ob = stripe_event_objects.Subscription(data)
    try:
        sub = Subscription.objects.get(stripe_id=sub_ob.subscription_id)
    except Subscription.DoesNotExist:
        raise Exception("Subscription not found for update with id: " + sub_ob.subscription_id)

    if(status != None):
        sub.status = status
    else:
        sub.status = getattr(parameters.Stripe.Subscription.Status,sub_ob.status)

    if(current_invoice_status != None):
        sub.invoice.status = current_invoice_status
        sub.invoice.save()

    sub.start_date = sub_ob.start_date
    sub.end_date = sub_ob.end_date
    sub.save()

def new_invoice(data):
    inv_ob = stripe_event_objects.Invoice(data)

    subs = Subscription.objects.filter(stripe_id = inv_ob.subscription_id)
    sub = None
    if(len(subs) > 0):
        sub = subs.last()
        if(sub.status == parameters.Stripe.Subscription.Status.canceled):
            return

    inv = get_invoice_skeleton(inv_ob)
    existing = Invoice.objects.filter(subscription_stripe_id=inv_ob.subscription_id)
    if(len(existing) > 0):
        prev_tk = existing.last().tk
        inv.tk = prev_tk + 1
    inv.save()

    if(sub != None):
        sub.invoice = inv
        sub.save()

def update_invoice(data):
    inv_ob = stripe_event_objects.Invoice(data)
    invoice = Invoice.objects.get(stripe_id = inv_ob.id)
    invoice.status = getattr(parameters.Stripe.Invoice.Status, inv_ob.status)
    if(invoice.status == parameters.Stripe.Invoice.Status.paid):
        tr = get_transaction_skeleton(inv_ob)
        tr.save()
        transactions.add_related(tr, inv_ob)
        transactions.update_product_revenues(tr)
        invoice.transaction = tr
    if(invoice.invoice == None):
        invoice.invoice = inv_ob.invoice
    
    if(invoice.transaction != None):
        invoice.transaction.save()
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
        invoice=ob.invoice,
        number=ob.number
    )

def get_transaction_skeleton(model):
    return Transaction(
        product=model.product,
        amount=model.price,
        type=parameters.Transaction.Type.purchase
    )

def get_purchase_skeleton(ob):
    return Purchase(
        user=ob.buyer,
        product=ob.product,
        activation_id=common.random_id()
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
    sub_ob = stripe_event_objects.Subscription(data)
    try:
        sub = Subscription.objects.get(stripe_id=sub_ob.subscription_id)
    except Subscription.DoesNotExist:
        raise Exception("Subscription not found for update with id: " + sub_ob.subscription_id)

    try:
        purchase = Purchase.objects.get(subscription=sub)
    except Purchase.DoesNotExist:
        raise Exception("Purchase not found for subscription update with id: " + sub_ob.subscription_id)

    sub.status = getattr(parameters.Stripe.Subscription.Status,sub_ob.status)

    if(sub.invoice.status != parameters.Stripe.Invoice.Status.paid):
        sub.invoice.status = parameters.Stripe.Invoice.Status.void
        sub.invoice.save()

    sub.cancel_date = sub_ob.cancel_date
    sub.cancel_reason = sub_ob.cancel_reason
    sub.save()

    purchase.status = parameters.Stripe.Purchase.Status.canceled
    purchase.save()

def application_deauthorized(data):
    account = data["account"]
    Stripe_account.objects.filter(account_id=account).delete()

def update_account(data):
    parsed_data = stripe_event_objects.Account(data)
    org = api_utils.get_organization_by_id(parsed_data.organization_id)
    if(org == None):
        raise Exception("Organization from account webhook not found in db")
    account = None
    try:
        account = Stripe_account.objects.get(account_id=parsed_data.id, organization=org)
    except Stripe_account.DoesNotExist:
        account = None
    if(account != None):
        #Update existing stripe account in organization
        account = parsed_data.update(account)
    else:
        #Insert new stripe account for organization
        account = parsed_data.insert(org)
    
    
    
