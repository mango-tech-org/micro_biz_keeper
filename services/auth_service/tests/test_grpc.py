import uuid

import grpc
import pytest
from auth_service.grpc_pb import auth_pb2_grpc, auth_pb2
from auth_service.grpc_server import AuthService
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def unique_phone_number():
    return f"2567{str(uuid.uuid4().int)[:9]}"


@pytest.fixture(scope="module")
def grpc_server():
    server = AuthService()
    server.add_insecure_port("[::]:50051")
    server.start()
    yield server
    server.stop(0)


@pytest.fixture(scope="module")
def grpc_channel():
    channel = grpc.insecure_channel("localhost:50051")
    yield channel


@pytest.mark.django_db
def test_user_registration(grpc_channel, unique_phone_number):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    response = stub.Register(
        auth_pb2.UserRegisterRequest(
            phone_number=unique_phone_number,
            password="testPassword",
            repeat_password="testPassword",
        )
    )
    assert response.message == "User registered successfully"
    assert response.user_id


@pytest.mark.django_db
def test_user_registration_password_mismatch(
    grpc_channel, unique_phone_number
):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)

    with pytest.raises(grpc.RpcError) as e:
        stub.Register(
            auth_pb2.UserRegisterRequest(
                phone_number=unique_phone_number,
                password="testPassword",
                repeat_password="wrongPassword",
            )
        )

    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert e.value.details() == "Passwords do not match"
    assert not User.objects.filter(
        phone_number=unique_phone_number
    ).exists()


@pytest.mark.django_db
def test_user_login(grpc_channel, unique_phone_number):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    # Register a user
    stub.Register(
        auth_pb2.UserRegisterRequest(
            phone_number=unique_phone_number,
            password="testPassword",
            repeat_password="testPassword",
        )
    )
    response = stub.Login(
        auth_pb2.UserLoginRequest(
            phone_number=unique_phone_number, password="testPassword"
        )
    )

    assert response.message == "Login successful"
    assert response.access_token
    assert response.refresh_token
