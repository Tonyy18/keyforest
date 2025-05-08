from rest_framework import serializers
from .models import Organization
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class OrganizationSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'description']