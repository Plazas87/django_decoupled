"""User views module."""


from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import CustomUserCreationForm, UserLoginForm

User = get_user_model()


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

            url = reverse("users:dashboard", kwargs={"pk": form.user_cache.id})

            return HttpResponseRedirect(url)

        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):
    """LogoutView class."""

    template: str = "users/logout.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle a GET request."""
        logout(request=request)

        return render(request, self.template)


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
            form.save()

            return HttpResponseRedirect(reverse("users:login"))

        return render(request, "users/register.html", {"form": form})


class UserViewList(LoginRequiredMixin, View):
    """UserViewList class."""

    template: str = "users/dashboard.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Handle a GET request."""
        users = User.objects.all()

        context = {"users": users}

        return render(request, self.template, context=context)
