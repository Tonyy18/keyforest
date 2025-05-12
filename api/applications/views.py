from django.shortcuts import render
from .serializers import ApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ApplicationsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, orgId):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)