from lib import parameters
from project.models import Transaction
from decimal import Decimal

def calc_transaction_net(tr: Transaction):
    related = tr.related.all()
    amount = 0
    for t in related:
        amount = amount + t.amount
    return Decimal(tr.amount) + Decimal(amount)

def update_product_revenues(transaction):
    amount = transaction.amount
    transaction.product.revenue += Decimal(amount)
    transaction.product.net_revenue += Decimal(calc_transaction_net(transaction))
    transaction.product.save()

def add_related(transaction, event_ob):
    if(event_ob.fee != None and event_ob.fee > 0.00):
        #Application fee
        tr = Transaction(
            product=transaction.product,
            amount=-abs(event_ob.fee),
            type=parameters.Transaction.Type.platform_fee
        )
        tr.save()
        transaction.related.add(tr)