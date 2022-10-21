import stripe
from . import authenticate
from project.models import License

authenticate(stripe)
#https://stripe.com/docs/api/products/create?lang=python
def createProduct(license):
    if(type(license) is not License):
        return None
    res = stripe.Product.create(
        name = license.name,
        default_price_data = {
            "currency": "USD",
            "unit_amount_decimal" = license.price
        }
    )
