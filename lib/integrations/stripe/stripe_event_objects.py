from project.models import License, User, Organization, Stripe_account
from lib.utils import common
from lib.integrations.stripe import stripe_api, stripe_charges
import json
#Each class contains the data parsed from Stripe webhook events

def get_main_data(data):
    if(type(data) is str):
        data = json.loads(data)
    if("object" in data):
        if(data["object"] == "event"):
            return data["data"]["object"]
        else:
            return data

class Invoice:
    def __parse(self, data):
        customer = data["subscription_details"]["metadata"]["user"]
        product_id = data["subscription_details"]["metadata"]["product"]
        self.id = data["id"]
        self.status = data["status"]
        self.created = common.epoch_to_date(data["created"])
        self.subscription_id = data["subscription"]
        self.invoice = data["hosted_invoice_url"]
        self.number = data["number"]
        self.price = common.cents_to_dollars(data["amount_due"])
        if(self.status == "paid"):
            self.price = common.cents_to_dollars(data["amount_paid"])
        try:
            self.fee = common.cents_to_dollars(data["application_fee_amount"])
        except:
            print(data)
        period = data["lines"]["data"][0]["period"]
        period_start = period["start"]
        period_end = period["end"]
        self.start_date = common.epoch_to_date(period_start)
        self.end_date = common.epoch_to_date(period_end)

        self.buyer = User.objects.get(id=customer)
        self.product = License.objects.get(id=product_id)
        if(self.buyer == None):
            raise Exception("Failed to retrieve user for invoice.paid event. customer id: " + str(customer))
        if(self.product == None):
            raise Exception("Failed to retrieve license for invoice.paid event. product id: " + str(product))

    def __init__(self, data):
        self.type = "invoice"
        self.data = get_main_data(data)
        self.__parse(self.data)
        if(not self.buyer):
            raise Exception("Payment object is missing required buyer property")
        if(not self.product):
            raise Exception("Payment object is missing required product property")
        if(not self.price):
            raise Exception("Payment object is missing required price property")
        if(not self.subscription_id):
            raise Exception("Payment object is missing required subscription id property")
        if(not self.created):
            raise Exception("Payment object is missing required created property")

class Payment:
    def __parse(self, data):
        self.created = common.epoch_to_date(data["created"])
        self.latest_charge = stripe_charges.get_charge(data["latest_charge"])
        self.receipt = self.latest_charge["receipt_url"]
        product_id = data["metadata"]["product"]
        user_id = data["metadata"]["user"]
        self.price = common.cents_to_dollars(data["amount"])
        self.fee = common.cents_to_dollars(data["application_fee_amount"])
        self.buyer = User.objects.get(id=user_id)
        self.product = License.objects.get(id=product_id)

    def __init__(self, data):
        self.type = "payment"
        self.data = get_main_data(data)
        self.__parse(self.data)
        if(not self.buyer):
            raise Exception("Payment object is missing required buyer property")
        if(not self.product):
            raise Exception("Payment object is missing required product property")
        if(not self.price):
            raise Exception("Payment object is missing required price property")
        if(not self.price):
            raise Exception("Payment object is missing required created property")

class Subscription:
    def __parse(self, data):
        customer = data["customer"]
        product = data["plan"]["product"]
        self.status = data["status"]
        if(self.status == "incomplete_expired"):
            self.status = "expired"
        self.subscription_id = data["id"]
        self.price = common.cents_to_dollars(data["items"]["data"][0]["price"]["unit_amount"])
        self.buyer = stripe_api.get_user_by_id(customer)
        self.product = stripe_api.get_license_by_id(product)
        self.start_date = common.epoch_to_date(data["current_period_start"])
        self.end_date = common.epoch_to_date(data["current_period_end"])
        cancel_date = data["canceled_at"]
        self.cancel_date = None
        if(cancel_date):
            self.cancel_date = common.epoch_to_date(cancel_date)
        self.cancel_reason = data["cancellation_details"]["reason"]
        if(self.buyer == None):
            raise Exception("Failed to retrieve user for invoice.paid event. customer id: " + str(customer))
        if(self.product == None):
            raise Exception("Failed to retrieve license for invoice.paid event. product id: " + str(product))
    
    def __init__(self, data):
        self.type = "subscription"
        self.data = get_main_data(data)
        self.__parse(self.data)
        if(not self.buyer):
            raise Exception("Payment object is missing required buyer property")
        if(not self.product):
            raise Exception("Payment object is missing required product property")
        if(not self.price):
            raise Exception("Payment object is missing required price property")
        if(not self.subscription_id):
            raise Exception("Payment object is missing required subscription id property")

class Account:
    def __parse(self, data):
        self.id = data["id"]
        self.support_phone = None
        self.support_email = None
        self.disabled_reason = None
        self.currently_due = None
        self.eventually_due = None
        self.past_due = None
        self.errors = None
        self.verification_disabled_reason = None
        self.verification_fields_needed = None
        self.metadata = {}
        self.organization_id = None
        self.details_submitted = False
        self.transfers_active = True
        self.created = None
        self.display_name = None

        if("details_submitted" in data):
            self.details_submitted = data["details_submitted"]

        if("created" in data):
            self.created = common.epoch_to_date(data["created"])
        
        if("display_name" in data):
            self.display_name = data["display_name"]
        elif("settings" in data and "dashboard" in data["settings"] and "display_name" in data["settings"]["dashboard"]):
            self.display_name = data["settings"]["dashboard"]["display_name"]

        if("business_profile" in data):
            self.support_phone = data["business_profile"]["support_phone"]
            self.support_email = data["business_profile"]["support_email"]
        else:
            if("support_phone" in data):
                self.support_phone = data["support_phone"]
            if("support_email" in data):
                self.support_email = data["support_email"]

        if("capabilities" in data and "transfers" in data["capabilities"]):
            self.transfers_active = data["capabilities"]["transfers"].lower() == "active"

        if("requirements" in data):
            self.disabled_reason = data["requirements"]["disabled_reason"]
            if(len(data["requirements"]["currently_due"]) > 0):
                self.currently_due = json.dumps(data["requirements"]["currently_due"])
            if(len(data["requirements"]["eventually_due"]) > 0):
                self.eventually_due = json.dumps(data["requirements"]["eventually_due"])
            if(len(data["requirements"]["past_due"]) > 0):
                self.past_due = json.dumps(data["requirements"]["past_due"])
            if(len(data["requirements"]["errors"]) > 0):
                self.errors = json.dumps(data["requirements"]["errors"])

        if("verification" in data):
            self.verification_disabled_reason = data["verification"]["disabled_reason"]
            if(len(data["verification"]["fields_needed"]) > 0):
                self.verification_fields_needed = json.dumps(data["verification"]["fields_needed"])

        if("metadata" in data):
            self.metadata = data["metadata"]
        if("organization_id" in self.metadata):
            self.organization_id = int(self.metadata["organization_id"])
        else:
            raise Exception("Organization metadata missin from account webhook")
    
    def exists(self):
        return Stripe_account.objects.filter(account_id=self.id).count() > 0

    def __set_db_values(self, db):
        db.support_phone = self.support_phone
        db.support_email = self.support_email
        db.disabled_reason = self.disabled_reason
        db.currently_due = self.currently_due
        db.eventually_due = self.eventually_due
        db.past_due = self.past_due
        db.errors = self.errors
        db.verification_disabled_reason = self.verification_disabled_reason
        db.verification_fields_needed = self.verification_fields_needed
        db.details_submitted = self.details_submitted
        db.transfers_active = self.transfers_active
        db.created = self.created
        db.display_name = self.display_name
        return db

    def insert(self, org: Organization):
        if(org == None):
            raise Exception("Organization cannot be null")
        db = Stripe_account()
        db.organization = org
        db.account_id = self.id
        obj = self.__set_db_values(db)
        obj.save()
        return obj

    def update(self, account: Stripe_account):
        if(account == None):
            raise Exception("Stripe account cannot be null")
        obj = self.__set_db_values(account)
        if(obj.default == True and obj.is_usable() == False):
            obj.default = False
        obj.save()
        return obj

    def __init__(self, data):
        self.type = "account"
        self.data = get_main_data(data)
        self.__parse(self.data)