from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime

class Organization(models.Model):
    name = models.TextField(null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="organizations/", default="organizations/default.png")
    about = models.TextField(null=True)
    website_link = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)
    applications = models.IntegerField(default=0)
    users = models.IntegerField(default=0)
    class Meta:
        db_table = "organizations"

class User_connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    permissions = models.TextField(null=True)
    added = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "user_connections"

class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "invitations"

class Application(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.TextField(null=False)
    api_id = models.TextField(null=False)
    bio = models.TextField(null=True)
    download_link = models.TextField(null=True)
    website_link = models.TextField(null=True)
    created = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "applications"

class License(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.TextField(null=False)
    api_id = models.TextField(null=False)
    bio = models.TextField(null=True)
    parameters = models.TextField(null=True)
    amount = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    expiration = models.DateField(null=True)
    price = models.FloatField(null=True)
    visible = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "licenses"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = "purchases"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="users/", default="users/default.jpg")
    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = "user_profiles"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Organization)
def create_user_connection(sender, instance, created, **kwargs):
    #When organization is created
    if created:
        if(instance.creator.profile.organization==None):
            instance.creator.profile.organization = instance
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