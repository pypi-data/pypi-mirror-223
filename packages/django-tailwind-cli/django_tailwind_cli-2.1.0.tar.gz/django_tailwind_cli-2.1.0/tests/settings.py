from __future__ import annotations

import pathlib
from tempfile import mkdtemp
from typing import Any

BASE_DIR = pathlib.Path(mkdtemp())

DEBUG = False

SECRET_KEY = "NOTASECRET"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django_tailwind_cli",
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"
STATICFILES_DIRS = (BASE_DIR / "assets",)

USE_TZ = True

SILENCED_SYSTEM_CHECKS = ["staticfiles.W004"]

TEST_RUNNER = "django_rich.test.RichRunner"
