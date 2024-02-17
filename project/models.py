from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from lib import parameters as params
import lib.utils as utils
from decimal import Decimal
import json

class Organization(models.Model):
    name = models.TextField(null=False, max_length=params.Organization.max_name_length)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="organization_creator",
        null=True
    )
    image = models.ImageField(upload_to="organizations/", default="organizations/default.png")
    about = models.TextField(null=True, max_length=params.Organization.max_bio_length)
    website_link = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)
    applications = models.IntegerField(default=0)
    users = models.IntegerField(default=0)

    class Meta:
        db_table = "organizations"

class Stripe_account(models.Model):

    def __init(self):
        self.json = False

    account_id = models.TextField()
    support_phone = models.TextField(null=True)
    support_email = models.TextField(null=True)
    disabled_reason = models.TextField(null=True)

    currently_due = models.TextField(null=True)
    eventually_due = models.TextField(null=True)
    past_due = models.TextField(null=True)
    errors = models.TextField(null=True)
    verification_fields_needed = models.TextField(null=True)

    verification_disabled_reason = models.TextField(null=True)
    details_submitted = models.BooleanField(default=False)
    transfers_active = models.BooleanField(default=False)
    created = models.DateField(null=True)
    default = models.BooleanField(default=False)
    display_name = models.TextField(null=True)
    organization = models.ForeignKey(
        Organization,
        null=True,
        on_delete=models.CASCADE
    )
    class Meta:
        db_table = "stripe_accounts"
    
    def get_actions_required_count(self):
        if(self.json == False):
            self.convert_json_fields()
        count = 0
        if(self.currently_due != None):
            count = count + len(self.currently_due)
        if(self.eventually_due != None):
            count = count + len(self.eventually_due)
        if(self.past_due != None):
            count = count + len(self.past_due)
        if(self.verification_fields_needed != None):
            count = count + len(self.verification_fields_needed)
        if(self.errors != None):
            count = count + len(self.errors)
        return count

    def convert_json_fields(self):
        self.json = True
        if(self.currently_due != None):
            self.currently_due = json.loads(self.currently_due)
        if(self.eventually_due != None):
            self.eventually_due = json.loads(self.eventually_due)
        if(self.past_due != None):
            self.past_due = json.loads(self.past_due)
        if(self.errors != None):
            self.errors = json.loads(self.errors)
        if(self.verification_fields_needed != None):
            self.verification_fields_needed = json.loads(self.verification_fields_needed)

    def is_usable(self):
        return self.transfers_active == True and self.disabled_reason == None and self.verification_disabled_reason == None and self.errors == None

class User(AbstractBaseUser):
    username = None
    first_name = models.TextField(null=False, max_length=params.User.max_firstname_length)
    last_name = models.TextField(null=False, max_length=params.User.max_lastname_length)
    password = models.TextField(null=False)
    email = models.CharField(null=False, unique=True, max_length=params.User.max_email_length)
    image = models.ImageField(upload_to="users/", default="users/default.jpg", unique=False)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)
    USERNAME_FIELD = 'email'
    email_confirmed = models.BooleanField(default=False)
    role = models.IntegerField(null=True)
    stripe_customer_id = models.TextField(null=True)
    class Meta:
        db_table = "users"

    def has_role(self, role):
        #parameter: Role.Admin, ...
        return self.role == role.role

class User_connection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    permissions = models.TextField(null=True, default="")
    added = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "user_connections"

class Application(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.TextField(null=False, max_length=params.Application.max_name_length)
    image = models.ImageField(upload_to="applications/", default="applications/default.png")
    api_key = models.UUIDField(default=uuid.uuid4, editable=False)
    bio = models.TextField(null=True, max_length=params.Application.max_bio_length)
    download_link = models.TextField(null=True)
    website_link = models.TextField(null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateField(auto_now_add=True)
    licenses = models.IntegerField(default=0)
    class Meta:
        db_table = "applications"

class License(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.TextField(null=False, max_length=params.License.max_name_length)
    image = models.ImageField(upload_to="licenses/", default="applications/default.png")
    api_key = models.UUIDField(default=uuid.uuid4, editable=False)
    bio = models.TextField(null=True, max_length=params.License.max_bio_length)
    parameters = models.TextField(null=True, default="{}")
    amount = models.IntegerField(null=True,validators=[
        MaxValueValidator(params.License.max_amount),
        MinValueValidator(1)
    ])
    subscription_period = models.IntegerField(null=True,validators=[
        MaxValueValidator(params.License.max_subscription_period),
        MinValueValidator(1)
    ])
    subscription_type = models.IntegerField(null=False, validators=[
        MaxValueValidator(len(params.License.Subscription_period_type.text)),
        MinValueValidator(0)
    ], default=0)
    expiration = models.DateField(null=True)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1)
    visible = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    stripe_product_id = models.TextField(null=True)
    stripe_price_id = models.TextField(null=True)
    revenue = models.DecimalField(null=False, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1, default=0.00)
    net_revenue = models.DecimalField(null=False, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1, default=0.00)
    stripe_account = models.ForeignKey(
        Stripe_account,
        on_delete=models.SET_NULL,
        null=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="license_creator",
        null=True
    )

    def get_stripe_account(self):
        #Should always be used to retrieve the stripe account
        account = self.stripe_account
        if(account == None):
            #user organizations default stripe account if not specified
            try:
                account = Stripe_account.objects.get(organization=self.application.organization, default=True)
            except Stripe_account.DoesNotExist:
                return None
        if(account.is_usable()):
            return account
            
    class Meta:
        db_table = "licenses"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(License, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1)
    date = models.DateField(null=False)
    receipt = models.TextField(null=True)
    transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = "payments"

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(License, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1)
    date = models.DateField(null=False)
    stripe_id = models.TextField(null=True)
    subscription_stripe_id = models.TextField(null=True)
    status = models.IntegerField(null=False)
    invoice = models.TextField(null=True)
    number = models.TextField(null=True)
    tk = models.IntegerField(null=False, default=1)
    transaction = models.ForeignKey("Transaction", on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "invoices"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(License, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    stripe_id = models.TextField(null=True)
    status = models.IntegerField(null=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    cancel_date = models.DateField(null=True)
    cancel_reason = models.TextField(null=True)
    cancel_at_period_end = models.BooleanField(null=False, default=False)
    class Meta:
        db_table = "subscriptions"

class Transaction(models.Model):
    product = models.ForeignKey(License, on_delete=models.CASCADE)
    amount = models.DecimalField(null=False, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1)
    type = models.IntegerField(null=False)
    date = models.DateField(auto_now_add=True)
    related = models.ManyToManyField("Transaction", null=True)
    class Meta:
        db_table = "transactions"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(License, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    activated = models.BooleanField(null=False, default=False)
    status = models.IntegerField(null=False, default=params.Stripe.Purchase.Status.not_activated)
    activation_id = models.TextField(null=False)
    activation_date = models.TextField(null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = "purchases"

    def is_activable(self):
        statuses = params.Stripe.Purchase.Status
        if(self.status == statuses.not_activated):
            if(self.subscription != None):
                statuses = params.Stripe.Subscription.Status
                if(self.subscription.status == statuses.active):
                    return True
            else:
                return True
        return False

    def is_cancellable(self):
        if(self.subscription == None and self.status != params.Stripe.Purchase.Status.canceled):
            return True
        if(self.subscription and self.subscription.cancel_at_period_end == False and (
            self.subscription.status == params.Stripe.Subscription.Status.active or 
            self.subscription.status == params.Stripe.Subscription.Status.past_due)):
            return True
    
        return False

    def get_status(self):
        status = ""
        if(self.product.subscription_type == params.License.Subscription_period_type.never or self.subscription.status == params.Stripe.Subscription.Status.active):
            if(self.subscription and self.subscription.cancel_at_period_end):
                status = "Cancels at " + str(utils.common.format_date(self.subscription.end_date))
            else:
                status = params.Stripe.Purchase.Status.text[self.status]
        else:
            #subscription
            status = params.Stripe.Subscription.Status.text[self.subscription.status]
        return status.capitalize()

    def get_next_invoice_status(self):
        text = ""
        if(self.product.subscription_type == params.License.Subscription_period_type.never or (self.subscription.status != params.Stripe.Subscription.Status.active or self.subscription.cancel_at_period_end)):
            text = "Not invoicing"
        else:
            text = utils.common.format_date(self.subscription.end_date)
        return text

@receiver(post_save, sender=Organization)
def create_user_connection(sender, instance, created, **kwargs):
    #When organization is created
    if created:
        instance.creator.organization = instance
        User_connection.objects.create(user=instance.creator, organization=instance, permissions="*")

@receiver(post_save, sender=User_connection)
def add_user_count(sender, instance, created, **kwargs):
    #When user connection is created
    if created:
        instance.organization.users += 1
        instance.organization.save()

@receiver(post_delete, sender=User_connection)
def delete_user_count(sender, instance, using, **kwargs):
    #When user connection is deleted
    instance.organization.users -= 1
    instance.organization.save()


@receiver(post_delete, sender=Application)
def delete_application_count(sender, instance, using, **kwargs):
    #When application is deleted
    instance.organization.applications -= 1
    instance.organization.save()

@receiver(post_save, sender=Application)
def add_application_count(sender, instance, created, **kwargs):
    #When application is created
    if created:
        instance.organization.applications += 1
        instance.organization.save()

@receiver(post_save, sender=License)
def add_license_count(sender, instance, created, **kwargs):
    #When license is created
    if created:
        instance.application.licenses += 1
        instance.application.save()

@receiver(post_delete, sender=License)
def delete_license_count(sender, instance, created, **kwargs):
    #When license is deleted
    if created:
        instance.application.licenses -= 1
        instance.application.save()