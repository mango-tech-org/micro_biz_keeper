import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

import pytest
from django.contrib.auth import get_user_model
from custom_auth.serializers import UserRegistrationSerializer, UserLoginSerializer
import uuid

User = get_user_model()


@pytest.fixture
def unique_phone_number():
    return f'2567{str(uuid.uuid4().int)[:9]}'  # Convert to string before slicing

@pytest.mark.django_db
def test_user_registration_serializer(unique_phone_number):
    # Test valid data
    data = {
        'phone_number': unique_phone_number,
        'password': 'testPassword'
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()

    assert user.phone_number == data['phone_number']
    assert user.check_password(data['password'])

    # Test missing password
    data = {
        'phone_number': '256758999982'
    }
    serializer = UserRegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert 'password' in serializer.errors


@pytest.mark.django_db
def test_user_login_serializer(unique_phone_number):
    user = User.objects.create_user(phone_number=unique_phone_number, password='testPassword')

    # Test valid data
    data = {
        'phone_number': unique_phone_number,
        'password': 'testPassword'
    }
    serializer = UserLoginSerializer(data=data)
    assert serializer.is_valid()
    tokens = serializer.save()

    assert 'access_token' in tokens
    assert 'refresh_token' in tokens

    # Test invalid password
    data = {
        'phone_number': unique_phone_number,
        'password': 'wrongPassword'
    }
    serializer = UserLoginSerializer(data=data)
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors

    
