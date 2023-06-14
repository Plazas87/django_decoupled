"""User mixin module."""
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class PasswordCheckMixin:
    """Mixin with password check and validation functionality."""

    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
        "duplicate_username": _("A user with that %(username)s already exists."),
    }

    def clean_password2(self) -> str:
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get("password1")  # type: ignore
        password2 = self.cleaned_data.get("password2")  # type: ignore
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch"
            )
        return password2

    def _post_clean(self) -> None:
        """Validate the password after self.instance is updated with form data by super()."""
        super()._post_clean()  # type: ignore
        password = self.cleaned_data.get("password2")  # type: ignore
        if password:
            try:
                password_validation.validate_password(password, self.instance)  # type: ignore
            except forms.ValidationError as error:
                self.add_error("password2", error)  # type: ignore
