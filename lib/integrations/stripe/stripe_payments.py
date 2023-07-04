from project.models import Checkout_session
from lib.integrations.stripe import stripe_api
from lib.utils import common
from lib.utils.api_utils import create_purchase

class Payment:
    def __parse_payment(self, data):
        customer = data["data"]["object"]["customer"]
        payment_id = data["data"]["object"]["id"]
        self.receipt = data["data"]["object"]["charges"]["data"][0]["receipt_url"]
        session = Checkout_session.objects.get(payment_id=payment_id)
        self.price = common.cents_to_dollars(data["data"]["object"]["amount"])
        self.buyer = session.buyer
        self.product = session.product
    
    def __parse_invoice(self, data):
        customer = data["data"]["object"]["customer"]
        product = data["data"]["object"]["lines"]["data"][0]["price"]["product"]
        self.invoice = data["data"]["object"]["hosted_invoice_url"]
        self.price = common.cents_to_dollars(data["data"]["object"]["lines"]["data"][0]["amount"])

        period = data["data"]["object"]["lines"]["data"][0]["period"]
        period_start = period["start"]
        period_end = period["end"]
        self.start_date = common.epoch_to_date(period_start)
        self.end_date = common.epoch_to_date(period_end)

        self.buyer = stripe_api.get_user_by_id(customer)
        self.product = stripe_api.get_license_by_id(product)
        if(self.buyer == None):
            raise Exception("Failed to retrieve user for invoice.paid event. customer id: " + str(customer))
        if(self.product == None):
            raise Exception("Failed to retrieve license for invoice.paid event. product id: " + str(product))
    

    def __init__(self, _type, data):
        self.type = _type
        self.data = data
        if(_type == "payment"):
            self.__parse_payment(data)
        elif(_type == "invoice"):
            self.__parse_invoice(data)
        if(not self.buyer):
            raise Exception("Payment object is missing required buyer property")
        if(not self.product):
            raise Exception("Payment object is missing required product property")
        if(not self.price):
            raise Exception("Payment object is missing required price property")

        print(self.product)

def payment_succeeded(data):
    payment = Payment("payment", data)
    create_purchase(payment)
    

def invoice_paid(data):
    payment = Payment("invoice", data)
    create_purchase(payment)
