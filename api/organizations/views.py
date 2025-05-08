from django.shortcuts import render
from .serializers import OrganizationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Organization
from users.models import UserConnection

class OrganizationsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            UserConnection(user=request.user, organization=organization).save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)