
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Permission
from .serializers import PermissionSerializer
from rest_framework.permissions import IsAuthenticated

class PermissionsView(APIView):

    def get(self, request):
        items = Permission.objects.all()
        serializer = PermissionSerializer(items, many=True)
        return Response(serializer.data)