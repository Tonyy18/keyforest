from project.models import Checkout_session
def payment_succeeded(data):
    customer = data["data"]["object"]["customer"]
    payment_id = data["data"]["object"]["id"]

    session = Checkout_session.objects.get(payment_id=payment_id)
    receiver = session.buyer
    product = session.product
    

def invoice_paid(data):
    pass