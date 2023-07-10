"""Users URLs module."""
from django.urls import path

from .views import LoginView, LogoutView, RegisterView, UserViewList

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("dashboard/<str:pk>", UserViewList.as_view(), name="dashboard"),
]
