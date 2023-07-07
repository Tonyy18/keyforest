from project.models import Checkout_session
from lib.utils import common
class Invoice:
    def __parse(self, data):
        customer = data["data"]["object"]["customer"]
        product = data["data"]["object"]["lines"]["data"][0]["price"]["product"]
        self.subscription_id = data["data"]["object"]["customer"]["subscription"]
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

    def __init__(self, data):
        self.type = "invoice"
        self.data = data
        self.__parse(data)
        if(not self.buyer):
            raise Exception("Payment object is missing required buyer property")
        if(not self.product):
            raise Exception("Payment object is missing required product property")
        if(not self.price):
            raise Exception("Payment object is missing required price property")
        if(not self.subscription_id):
            raise Exception("Payment object is missing required subscription id property")

class Payment:
    def __parse(self, data):
        customer = data["data"]["object"]["customer"]
        payment_id = data["data"]["object"]["id"]
        self.receipt = data["data"]["object"]["charges"]["data"][0]["receipt_url"]
        session = Checkout_session.objects.get(payment_id=payment_id)
        self.price = common.cents_to_dollars(data["data"]["object"]["amount"])
        self.buyer = session.buyer
        self.product = session.product

    def __init__(self, data):
        self.type = "payment"
        self.data = data
        self.__parse(data)
        if(not self.buyer):
            raise Exception("Payment object is missing required buyer property")
        if(not self.product):
            raise Exception("Payment object is missing required product property")
        if(not self.price):
            raise Exception("Payment object is missing required price property")

class Subscription:
    def __parse(self, data):
        customer = data["data"]["object"]["customer"]
        product = data["data"]["object"]["lines"]["plan"]["product"]
        self.subscription_id = data["data"]["object"]["items"]["data"][0]["price"]["subscription"]
        self.price = common.cents_to_dollars(data["data"]["object"]["lines"]["data"][0]["amount"])
        self.buyer = stripe_api.get_user_by_id(customer)
        self.product = stripe_api.get_license_by_id(product)
        if(self.buyer == None):
            raise Exception("Failed to retrieve user for invoice.paid event. customer id: " + str(customer))
        if(self.product == None):
            raise Exception("Failed to retrieve license for invoice.paid event. product id: " + str(product))

    def __init__(self, data):
        self.type = "subscription"
        self.data = data
        self.__parse(data)
        if(not self.buyer):
            raise Exception("Payment object is missing required buyer property")
        if(not self.product):
            raise Exception("Payment object is missing required product property")
        if(not self.price):
            raise Exception("Payment object is missing required price property")
        if(not self.subscription_id):
            raise Exception("Payment object is missing required subscription id property")