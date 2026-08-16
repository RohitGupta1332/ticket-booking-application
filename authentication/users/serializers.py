from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 8)

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'phone',
            'password'
        ]

    def create(self, validated_data):
        user = User(
            name = validated_data['name'],
            email = validated_data['email'],
            phone = validated_data['phone']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            username = email,
            password = password
        )

        if user is None:
            raise serializers.ValidationError('Invalid username or password')
        
        refresh = RefreshToken.for_user(user)

        return {
            'access' : str(refresh.access_token),
            'refresh' : str(refresh)
        }