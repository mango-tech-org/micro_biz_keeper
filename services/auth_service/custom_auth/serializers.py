from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from custom_auth.models import User


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = User.objects.filter(phone_number=phone_number).first()

            if user and user.check_password(password):
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid phone number or password.')
        else:
            raise serializers.ValidationError('Must include "phone_number" and "password".')

        return data

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user