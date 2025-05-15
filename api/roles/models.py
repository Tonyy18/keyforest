from django.db import models

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table  = "permissions"