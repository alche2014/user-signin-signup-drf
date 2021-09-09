from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.generics import CreateAPIView
from .serializers import UserLoginSerializers, UserSignupSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions


class ProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user.username),
            'auth': str(request.auth),
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_id': user.pk,
            'email': user.email,
            'password': user.password,
        })


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializers

    def post(self, request, format=None):
        data = request.data
        user_serilaizer = UserLoginSerializers(data=data)
        if user_serilaizer.is_valid(raise_exception=True):
            new_data = user_serilaizer.data
            return Response(new_data, status=HTTP_200_OK)
        else:
            return Response({"msg": "invalid user"}, status=HTTP_400_BAD_REQUEST)


class UserSignupView(CreateAPIView):

    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSignupSerializer
