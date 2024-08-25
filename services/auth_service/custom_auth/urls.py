from custom_auth.views import UserLoginView, UserRegistrationView
from django.urls import path

urlpatterns = [
    path(
        "register/",
        UserRegistrationView.as_view(),
        name="register-user",
    ),
    path("login/", UserLoginView.as_view(), name="login-user"),
]
