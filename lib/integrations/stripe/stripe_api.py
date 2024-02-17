from project.models import License, User

def get_license_by_id(id):
    try:
        prod = License.objects.get(stripe_product_id=id)
        return prod
    except License.DoesNotExist:
        return None

def get_user_by_id(id):
    try:
        prod = User.objects.get(stripe_customer_id=id)
        return prod
    except User.DoesNotExist:
        return None