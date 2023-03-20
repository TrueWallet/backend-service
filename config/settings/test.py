"""
With these settings, tests run faster.
"""
import logging
import os

from .base import *  # noqa

# from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

MEDIA_ROOT = os.path.join(APPS_DIR, "..", "test_media")  # noqa F405
STATIC_ROOT = os.path.join(APPS_DIR, "..", "test_public")  # noqa F405


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# This is because `django-log-request-id` was added.
logging.disable(logging.CRITICAL)
