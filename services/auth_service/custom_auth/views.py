import os

from django.contrib.auth import get_user_model
import dotenv
from rest_framework import generics, serializers, status, viewsets
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer

User = get_user_model()

dotenv.load_dotenv()

oauth2_client_id = os.getenv("OAUTH2_CLIENT_ID")
oauth2_client_secret = os.getenv("OAUTH2_CLIENT_SECRET")


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "phone_number", "is_staff"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
