"""
Django settings for django_decoupled project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
# pylint: disable=R0801
import os
from pathlib import Path
from typing import List

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# GENERAL > SECRETS
# ------------------------------------------------------------------------------

ALLOWED_HOSTS: List[str] = []

# Application definition
THIRD_PARTY_APPS: List[str] = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "pygmentify",
    "whitenoise.runserver_nostatic",
]

LOCAL_APPS: List[str] = [
    "django_decoupled.controllers.apps.users.apps.UsersConfig",
    "django_decoupled.controllers.apps.workspaces.apps.WorkspacesConfig",
]
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_decoupled.controllers.config.urls"

LOGIN_REDIRECT_URL = "/workspaces/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "django_decoupled.controllers.config.wsgi.application"

# GENERAL > DATABASES
# ------------------------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["PG_NAME"],
        "USER": os.environ["PG_USER"],
        "PASSWORD": os.environ["PG_PASSWORD"],
        "HOST": os.environ["PG_HOST"],
        "PORT": os.environ["PG_PORT"],
    }
}


# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CUSTOM USER MODEL
AUTH_USER_MODEL = "users.User"
# https://django-guardian.readthedocs.io/en/stable/configuration.html#anonymous-user-name
# Anonymous user name = None because is not allowed anonymous users in the project.
ANONYMOUS_USER_NAME = None


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Sites
SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# DJANGO ALLOUTH
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60

# FLUX PROJECT
FLUX_TRAIN_ENDPOINT_URL = os.environ["FLUX_TRAIN_ENDPOINT_URL"]
FLUX_TRAIN_ENDPOINT_METHOD = os.environ["FLUX_TRAIN_ENDPOINT_METHOD"]
FLUX_METRICS_ENDPOINT_URL = os.environ["FLUX_METRICS_ENDPOINT_URL"]
FLUX_METRICS_ENDPOINT_METHOD = os.environ["FLUX_METRICS_ENDPOINT_METHOD"]

# REQUESTOR
REQUESTOR_AVAILABLE_HTTP_METHODS = os.environ["AVAILABLE_HTTP_METHODS"]