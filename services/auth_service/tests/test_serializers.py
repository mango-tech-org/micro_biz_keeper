import uuid

import pytest
from custom_auth.serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def unique_phone_number():
    return f"2567{str(uuid.uuid4().int)[:9]}"


@pytest.mark.django_db
def test_user_registration_serializer(unique_phone_number):
    # Test valid data
    data = {
        "phone_number": unique_phone_number,
        "password": "testPassword",
        "repeat_password": "testPassword",
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()

    assert user.phone_number == data["phone_number"]
    assert user.check_password(data["password"])

    # Test missing password
    data = {"phone_number": "256758999982"}
    serializer = UserRegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors

    # Test password mismatch
    data = {
        "phone_number": "256758999982",
        "password": "testPassword",
        "repeat_password": "wrongPassword",
    }
    serializer = UserRegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert (
        "repeat_password" in serializer.errors
    ), "Expected 'repeat_password' error message"
