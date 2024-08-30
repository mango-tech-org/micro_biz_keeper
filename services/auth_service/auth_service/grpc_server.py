# auth_service/grpc_server.py
import os
import sys
from concurrent import futures

import django
from dotenv import load_dotenv
import grpc

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_service.settings")
django.setup()
from django.contrib.auth import get_user_model  # noqa: E402
from grpc_reflection.v1alpha import reflection  # noqa: E402
from rest_framework_simplejwt.tokens import (  # noqa: E402
    RefreshToken,
    TokenError,
)

from auth_service.grpc_pb import auth_pb2, auth_pb2_grpc  # noqa: E402

load_dotenv()

OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")

User = get_user_model()


class AuthService(auth_pb2_grpc.AuthServiceServicer):

    def Register(self, request, context):
        try:
            if request.password != request.repeat_password:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Passwords do not match")
                return auth_pb2.UserRegisterResponse(
                    user_id="",
                    message="Passwords do not match",
                )
            user = User.objects.create_user(
                phone_number=request.phone_number,
                password=request.password,
            )
            return auth_pb2.UserRegisterResponse(
                user_id=str(user.id),
                message="User registered successfully",
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to register user: {str(e)}")
            return auth_pb2.UserRegisterResponse(
                user_id="",
                message=f"Failed to register user: {str(e)}",
            )

    def Login(self, request, context):
        try:
            user = User.objects.get(phone_number=request.phone_number)
            if user.check_password(request.password):
                refresh = RefreshToken.for_user(user)
                return auth_pb2.UserLoginResponse(
                    access_token=str(refresh.access_token),
                    refresh_token=str(refresh),
                    message="Login successful",
                )
            else:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details("Invalid credentials")
                return auth_pb2.UserLoginResponse(
                    access_token="",
                    refresh_token="",
                    message="Invalid credentials",
                )
        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return auth_pb2.UserLoginResponse(
                access_token="",
                refresh_token="",
                message="User not found",
            )

    def RefreshToken(self, request, context):
        try:
            refresh = RefreshToken(request.refresh_token)
            new_access_token = refresh.access_token
            return auth_pb2.RefreshTokenResponse(
                access_token=str(new_access_token),
                message="Token refreshed successfully",
            )
        except TokenError as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(f"Failed to refresh token: {str(e)}")
            return auth_pb2.RefreshTokenResponse(
                access_token="",
                message=f"Failed to refresh token: {str(e)}",
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)

    SERVICE_NAMES = (
        reflection.SERVICE_NAME,
        auth_pb2.DESCRIPTOR.services_by_name["AuthService"].full_name,
    )

    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
