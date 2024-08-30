from custom_auth.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "password", "repeat_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError(
                {"repeat_password": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("repeat_password")
        user = User.objects.create_user(**validated_data)
        return user
