from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from lib import parameters as params

class Organization(models.Model):
    name = models.TextField(null=False, max_length=params.Organization.max_name_length)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_creator"
    )
    image = models.ImageField(upload_to="organizations/", default="organizations/default.png")
    about = models.TextField(null=True, max_length=params.Organization.max_bio_length)
    website_link = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)
    applications = models.IntegerField(default=0)
    users = models.IntegerField(default=0)
    class Meta:
        db_table = "organizations"

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

class Invitation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender_user"
    )
    class Meta:
        db_table = "invitations"

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
        MaxValueValidator(len(params.License.subscription_types)),
        MinValueValidator(0)
    ], default=0)
    expiration = models.DateField(null=True)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1)
    visible = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    stripe_product_id = models.TextField(null=True)
    stripe_price_id = models.TextField(null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="license_creator"
    )
    class Meta:
        db_table = "licenses"

class Checkout_session(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(License, on_delete=models.CASCADE)
    created = models.DateField(null=True)
    session_id =  models.TextField(null=False)
    payment_id = models.TextField(null=True)
    status = models.IntegerField(null=False)
    class Meta:
        db_table = "checkout_sessions"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(License, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, decimal_places=2, max_digits=len(str(params.License.max_price)) - 1)
    date = models.DateField(auto_now_add=True)
    receipt = models.TextField(null=True)
    invoice = models.TextField(null=True) #used with subscriptions
    class Meta:
        db_table = "payments"

class Purchase(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(License, on_delete=models.CASCADE)
    start = models.DateField(null=False)
    end = models.DateField(null=True)
    period_tk = models.IntegerField(null=False) #identifies recurring purchases
    period_id = models.IntegerField(null=False) #identifies the purchase
    activated = models.BooleanField(null=False, default=False)
    expired = models.BooleanField(null=True, default=False)
    activation_id = models.TextField(null=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    stripe_sub_id = models.TextField(null=True)
    class Meta:
        db_table = "purchases"

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
def add_user_count(sender, instance, created, **kwargs):
    #When application is created
    if created:
        instance.organization.applications += 1
    instance.organization.save()

@receiver(post_save, sender=License)
def add_license_count(sender, instance, created, **kwargs):
    #When application is created
    if created:
        instance.application.licenses += 1
    instance.application.save()

@receiver(post_delete, sender=License)
def delete_license_count(sender, instance, created, **kwargs):
    #When application is created
    if created:
        instance.application.licenses -= 1
    instance.application.save()