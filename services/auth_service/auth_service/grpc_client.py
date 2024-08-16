import grpc
from grpc_pb import auth_pb2, auth_pb2_grpc

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('10.97.29.40:50051') as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        
        # Test the Register method
        response = stub.Register(auth_pb2.UserRegisterRequest(phone_number="256712345678", password="testpassword123"))
        print("Register Response:", response.message)
        
        # Test the Login method
        response = stub.Login(auth_pb2.UserLoginRequest(phone_number="256712345678", password="testpassword123"))
        print("Login Response:", response.message)
        print("Access Token:", response.access_token)
        print("Refresh Token:", response.refresh_token)
        
        # Test the RefreshToken method
        response = stub.RefreshToken(auth_pb2.RefreshTokenRequest(refresh_token=response.refresh_token))
        print("Refresh Token Response:", response.message)
        print("New Access Token:", response.access_token)

if __name__ == '__main__':
    run()
