from custom_auth.views import UserRegistrationView
from django.urls import path
from oauth2_provider.views import TokenView

urlpatterns = [
    path(
        "register/",
        UserRegistrationView.as_view(),
        name="register-user",
    ),
    path("o/token/", TokenView.as_view(), name="token"),
]
