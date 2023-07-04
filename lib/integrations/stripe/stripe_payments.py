from project.models import Checkout_session
from lib.integrations.stripe import stripe_api
from lib.utils import common
def payment_succeeded(data):
    customer = data["data"]["object"]["customer"]
    payment_id = data["data"]["object"]["id"]
    receipt = data["data"]["object"]["charges"]["data"][0]["receipt_url"]
    session = Checkout_session.objects.get(payment_id=payment_id)
    receiver = session.buyer
    product = session.product
    

def invoice_paid(data):
    customer = data["data"]["object"]["customer"]
    product = data["data"]["object"]["lines"]["data"][0]["price"]["product"]
    invoice = data["data"]["object"]["hosted_invoice_url"]

    period = data["data"]["object"]["lines"]["data"][0]["period"]
    period_start = period["start"]
    period_end = period["end"]
    start_date = common.epoch_to_date(period_start)
    end_date = common.epoch_to_date(period_end)

    user = stripe_api.get_user_by_id(customer)
    license = stripe_api.get_license_by_id(product)
    if(user == None):
        raise Exception("Failed to retrieve user for invoice.paid event. customer id: " + str(customer))
    if(license == None):
        raise Exception("Failed to retrieve license for invoice.paid event. product id: " + str(product))
    
