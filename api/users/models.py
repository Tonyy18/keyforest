from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100, unique=True)
    password = models.TextField()

    class Meta:
        db_table  = "users"