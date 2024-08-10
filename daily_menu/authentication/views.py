from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework.request import Request
from rest_framework import status

from .serializers import (
    RegisterUserSerializer, 
    UserSerializer
)


User = get_user_model()


class CreateUserAPIView(APIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class UserAPIView(APIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer  = self.serializer_class(instance=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
