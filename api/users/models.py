from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from organizations.models import Organization

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100, unique=True)
    password = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    class Meta:
        db_table  = "users"

class UserConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table  = "user_connections"
