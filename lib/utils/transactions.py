from lib import parameters
from project.models import Transaction

def get_platform_fee_transaction(model):
    amount = -(model.price / 100) * parameters.Transaction.platform_fee
    tr = Transaction(
        product=model.product,
        amount=amount,
        type=parameters.Transaction.Type.platform_fee
    )
    return tr