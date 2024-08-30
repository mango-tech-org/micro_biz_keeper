import uuid

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from oauth2_provider.models import Application
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def unique_phone_number():
    return f"2567{str(uuid.uuid4().int)[:9]}"


@pytest.mark.django_db
def test_user_registration(api_client, unique_phone_number):
    # Register a user with a unique phone number
    url = reverse("register-user")
    payload = {
        "phone_number": unique_phone_number,
        "password": "testpassword123",
        "repeat_password": "testpassword123",
    }
    response = api_client.post(url, payload)
    assert response.status_code == 201
    assert User.objects.filter(
        phone_number=payload["phone_number"]
    ).exists()


@pytest.fixture
def oauth2_application():
    return Application.objects.create(
        name="Test Application",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        redirect_uris="http://localhost",
    )


@pytest.mark.django_db
def test_user_login(api_client, unique_phone_number, oauth2_application):
    # Create a user with a unique phone number
    User.objects.create_user(
        phone_number=unique_phone_number, password="testPassword"
    )

    assert User.objects.filter(phone_number=unique_phone_number).exists()

    url = reverse("oauth2_provider:authorize")
    data = {
        "client_id": oauth2_application.client_id,
        "response_type": "code",
        "redirect_uri": oauth2_application.redirect_uris,
        "state": "random state",
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db
def test_user_registration_password_mismatch(
    api_client, unique_phone_number
):
    url = reverse("register-user")
    payload = {
        "phone_number": unique_phone_number,
        "password": "testpassword123",
        "repeat_password": "testpassword",
    }
    response = api_client.post(url, payload)
    assert response.status_code == 400
    assert "repeat_password" in response.data
    assert not User.objects.filter(
        phone_number=payload["phone_number"]
    ).exists()
