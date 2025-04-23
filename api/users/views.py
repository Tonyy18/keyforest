from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


class UsersView(APIView):
    def get(self, request):
        items = User.objects.all()
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)