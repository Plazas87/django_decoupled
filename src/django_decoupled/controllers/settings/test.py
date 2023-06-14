"""django_decoupled Django aplication test setting module."""
from .base import *  # pylint: disable=W0401,W0614

SECRET_KEY = "#hcfe86ax6j1(s4!7bytvutw587+$we(**ex945@5j+0d=#2l="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

MIGRATION_MODULES = {"gazetteer": None}

# DATABASE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_django_decoupled_database",
    }
}
