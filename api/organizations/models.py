from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.CharField(max_length=400)

    class Meta:
        db_table  = "organizations"