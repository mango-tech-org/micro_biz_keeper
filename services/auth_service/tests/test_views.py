import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
import uuid

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def unique_phone_number():
    return f'2567{str(uuid.uuid4().int)[:9]}'  # Convert to string before slicing

@pytest.mark.django_db
def test_user_registration(api_client, unique_phone_number):
    # Register a user with a unique phone number
    url = reverse('register-user')
    payload = {
        'phone_number': unique_phone_number,
        'password': 'testpassword123'
    }
    response = api_client.post(url, payload)
    assert response.status_code == 201
    assert User.objects.filter(phone_number=payload['phone_number']).exists()

@pytest.mark.django_db
def test_user_login(api_client, unique_phone_number):
    # Create a user with a unique phone number
    user = User.objects.create_user(phone_number=unique_phone_number, password='testPassword')

    url = reverse('login-user')
    payload = {
        'phone_number': unique_phone_number,
        'password': 'testPassword'
    }
    response = api_client.post(url, payload)
    assert response.status_code == 200
    assert 'access_token' in response.data
    assert 'refresh_token' in response.data
