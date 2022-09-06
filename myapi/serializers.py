from rest_framework import serializers
from myapi.models import User

class UserResponseSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 
            'created_at', 'updated_at'
            
        ]

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(max_length=256, required=True)

class LoginResponseSerializer(serializers.Serializer):
    
    class TokensSerializer(serializers.Serializer):
        access_token = serializers.CharField(max_length=2000, required=True)
        refresh_token = serializers.CharField(max_length=2000, required=True)

    user = UserResponseSerializer()
    tokens = TokensSerializer()

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'password']


class ResetUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256)

    class Meta:
        fields = ['email']