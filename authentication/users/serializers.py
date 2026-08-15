from rest_framework import serializers
from .models import User

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