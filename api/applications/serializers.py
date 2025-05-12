from rest_framework import serializers
from .models import Application
from rest_framework.validators import UniqueValidator

class ApplicationSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Application
        fields = ['id', 'name', 'description']