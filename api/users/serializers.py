from rest_framework import serializers
from .models import User, UserConnection
from organizations.serializers import OrganizationSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserConnectionSerializer(serializers.ModelSerializer):

    userId = serializers.IntegerField(write_only=True, source='user_id')
    organizationId = serializers.IntegerField(write_only=True,source='organization_id')
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = UserConnection
        fields = ['id', 'userId', 'organizationId', 'organization']

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    connections = UserConnectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'email', 'password', 'connections']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user data
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'firstName': self.user.firstName,
            'lastName': self.user.lastName,
            # add more if needed
        }

        return data