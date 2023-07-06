"""User forms module."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .mixins import PasswordCheckMixin


class CustomUserCreationForm(PasswordCheckMixin, forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    class Meta:
        """Meta class."""

        model = get_user_model()
        fields = (get_user_model().USERNAME_FIELD,) + tuple(
            get_user_model().REQUIRED_FIELDS,
        )

    def __init__(self, *args, **kwargs) -> None:
        """Initialize Usercreationform."""
        super().__init__(*args, **kwargs)

    def save(self, commit: bool = True) -> "CustomUserCreationForm":
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if "is_active" in self.cleaned_data:
            user.is_active = self.cleaned_data["is_active"]

        if commit:
            user.save()
        return user


class CustomUserChangeForm(PasswordCheckMixin, UserChangeForm):
    """CustomUserChangeForm class."""

    class Meta:
        """Meta class."""  # noqa: D401

        model = get_user_model()
        fields = ("email",)


class UserLoginForm(AuthenticationForm):
    """UserLogin from class."""

    def clean(self):
        """Authenticate clean method."""
        # TODO Validate username and password using domain validators
        # username = self.cleaned_data.get("username")
        # password = self.cleaned_data.get("password")

        # Django authenticate
        cleaned_data = super().clean()

        return cleaned_data
