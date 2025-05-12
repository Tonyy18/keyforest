from django.db import models
from organizations.models import Organization

# Create your models here.
class Application(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=400, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table  = "applications"