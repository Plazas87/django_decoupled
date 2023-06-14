"""User admin module."""
from typing import Tuple

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """CustomUserAdmin class."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = ((None, {"fields": ("first_name", "last_name", "email", "password")}),)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    permission_fieldsets_for_superuser = (
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    permission_fieldsets_for_user = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    importantdates_fieldsets = (
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = (
        "is_active",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )

    list_display_links = ("email",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_fieldsets(self, request: HttpRequest, obj=None):
        """Return the fieldsets according to the kind of logged user."""
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            if obj.is_superuser:
                return (
                    self.fieldsets
                    + self.permission_fieldsets_for_superuser
                    + self.importantdates_fieldsets
                )

            return (
                self.fieldsets
                + self.permission_fieldsets_for_superuser
                + self.importantdates_fieldsets
            )

        if self.has_change_permission(request, obj):
            return self.fieldsets + self.permission_fieldsets_for_user

        return self.fieldsets

    def get_queryset(self, request):
        """Filter the data to be shown in the admin by User."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def get_list_display(self, request: HttpRequest) -> Tuple[str, ...]:
        """Prepare the list diaplay base on the user."""
        if request.user.is_superuser:
            return self.list_display

        return ("email", "first_name", "last_name")


admin.site.register(User, CustomUserAdmin)
