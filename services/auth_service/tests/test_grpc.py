import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

import pytest
import grpc
from auth_service.grpc_pb import auth_pb2, auth_pb2_grpc
from django.contrib.auth import get_user_model
from concurrent import futures
from auth_service.grpc_server import AuthService
import uuid

User = get_user_model()


@pytest.fixture
def unique_phone_number():
    return f'2567{str(uuid.uuid4().int)[:9]}'  # Convert to string before slicing

@pytest.fixture(scope='module')
def grpc_server():
    server = AuthService()
    server.add_insecure_port('[::]:50051')
    server.start()
    yield server
    server.stop(0)

@pytest.fixture(scope='module')
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel

@pytest.mark.django_db
def test_user_registration(grpc_channel, unique_phone_number):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    response = stub.Register(auth_pb2.UserRegisterRequest(phone_number=unique_phone_number, password='testPassword'))


    assert response.message == "User registered successfully"
    assert response.user_id
    assert User.objects.filter(phone_number=unique_phone_number).exists()

@pytest.mark.django_db
def test_user_login(grpc_channel, unique_phone_number):
    user = User.objects.create_user(phone_number=unique_phone_number, password='testPassword')

    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    response = stub.Login(auth_pb2.UserLoginRequest(phone_number=unique_phone_number, password='testPassword'))

    assert response.message == "Login successful"
    assert response.access_token
    assert response.refresh_token