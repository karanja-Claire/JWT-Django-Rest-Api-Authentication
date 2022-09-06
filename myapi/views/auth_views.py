from rest_framework import generics,status
from rest_framework import serializers
from myapi.models import User
from myapi.serializers import LoginResponseSerializer, LoginSerializer, RegisterUserSerializer
from rest_framework.response import Response
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken

from myapi.services.authentication_services import UserService

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    user_service = UserService()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        
        self.user_service.register_user(data)
        user = User.objects.create_user(
            username = data.get('first_name')+ " "+data.get('last_name'),
            first_name=data.get('first_name'),
            last_name = data.get('last_name'),
            email = data.get('email'),
            password = data.get('password')
        )
        serialized_data = self.serializer_class(user)
        return Response(
            data=serialized_data.data,
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            user = User.objects.get(
                email=data.get('email')
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                detail={'email': ['email does not exist']},
                code=400
            )
       
        user = auth.authenticate(email=user.email, password=data.get('password'))
        
        if not user:
            raise serializers.ValidationError(
                detail={'password': ['Invalid password']},
                code=401
            )
        tokens = RefreshToken.for_user(user)
        kwargs = {'user': user, 'tokens': {
            'refresh_token': str(tokens),
            'access_token': str(tokens.access_token)
        }}
        self.serializer_class = LoginResponseSerializer
        serialized_data = self.serializer_class(kwargs)
        return Response(
            data=serialized_data.data,
            status=status.HTTP_200_OK
        )