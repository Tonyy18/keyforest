import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_APIKEY
from lib.integrations.stripe import stripe_test_clocks, stripe_event_objects
from lib import parameters
from project.models import Stripe_account
import json

#https://stripe.com/docs/connect/collect-then-transfer-guide

def create_account(org):
    if(org == None):
        raise Exception("Organization cannot be null")
    return stripe.Account.create(type="standard", metadata={
        "organization_id": org.id
    })

def delete_account(account_id):
    if(type(account_id) is Stripe_account):
        account_id = account_id.account_id
    if(account_id == None):
        raise Exception("Account id cannot be null")
    response = stripe.Account.delete(account_id)
    return response["deleted"]

def get_account(account_id):
    if(type(account_id) is Stripe_account):
        account_id = account_id.account_id
    if(account_id == None):
        raise Exception("Account id cannot be null")
    return stripe.Account.retrieve(account_id)

def get_connected_accounts(limit = 100):
    return stripe.Account.list(limit=limit)

def link_account(user, account_id):
    return stripe.AccountLink.create(
        account=account_id,
        return_url=parameters.Server.url + "/dashboard/organization/" + str(user.organization.id) + "/stripe",
        refresh_url=parameters.Server.url + "/dashboard/organization/" + str(user.organization.id) + "/stripe",
        type="account_onboarding",
    )