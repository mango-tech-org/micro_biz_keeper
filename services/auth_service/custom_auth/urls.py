from django.urls import path
from custom_auth.views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register-user'),
    path('login/', UserLoginView.as_view(), name='login-user'),
]