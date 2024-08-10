from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import (
    RegisterUserSerializer, 
    UserSerializer
)


User = get_user_model()


class CreateUserAPIView(APIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serialzier = self.serializer_class(data=request.data)

        if not serialzier.is_valid():
            return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serialzier.save()
        return Response(status=status.HTTP_201_CREATED)


class UserAPIView(APIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serialzier  = self.serializer_class(instance=request.user)
        return Response(data=serialzier.data, status=status.HTTP_200_OK)
