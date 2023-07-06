"""User views module."""


from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import CustomUserCreationForm, UserLoginForm


class LoginView(auth_views.LoginView):
    """LoginView class."""

    template_name = "users/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle a GET request."""
        form = self.authentication_form()

        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle a POST request."""
        form = self.authentication_form(data=request.POST)

        # The form perform the authentication process when calling is_valid()
        if form.is_valid():
            # Load the current authenticated user into session
            login(request=request, user=form.user_cache)

        return HttpResponseRedirect(reverse("workspaces:file-upload"))


class RegisterView(View):
    """RegisterView class."""

    template = "users/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle a GET request."""
        form = CustomUserCreationForm()

        return render(request, self.template, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle a POST request."""
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            print("@@@@@")

        return render(request, "users/register.html", {"form": form})
