"""
Django settings for config project.

Environment variables (via backend/.env or shell environment) control all
sensitive and deployment-specific values. See backend/.env.example for the
complete list of supported variables.
"""

import os
import sys
import urllib.parse
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY — All secrets come from environment variables only
# ============================================================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    if "test" in sys.argv:
        # Use a safe dummy key only when running the automated test suite
        SECRET_KEY = "test-only-insecure-key-not-for-production-use"
    else:
        raise RuntimeError(
            "DJANGO_SECRET_KEY environment variable is not set. "
            "Set it in backend/.env or in your shell environment before "
            "starting the server. See backend/.env.example for instructions."
        )


# ============================================================
# YOJANASAATHI AI AGENT CONFIGURATION
# ============================================================

# Secret key for machine-to-machine AI agent authentication fallback
YOJANASAATHI_AGENT_API_KEY = os.getenv("YOJANASAATHI_AGENT_API_KEY", "")


# ============================================================
# DEBUG MODE
# ============================================================

# Set DEBUG=False (or omit) in production.
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ("true", "1", "yes")


# ============================================================
# HOSTS AND ORIGINS
# ============================================================

_allowed_hosts_raw = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(",") if h.strip()]

_cors_raw = os.getenv(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)
CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_raw.split(",") if o.strip()]

# Allow custom headers for AI agent and citizen delegation in CORS
CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-agent-api-key",
    "x-citizen-delegation-token",
]

_csrf_raw = os.getenv(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_raw.split(",") if o.strip()]


# ============================================================
# TWILIO OTP CONFIGURATION
# ============================================================

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_VERIFY_SERVICE_SID = os.getenv("TWILIO_VERIFY_SERVICE_SID", "")
TWILIO_ALLOWED_MOBILE = os.getenv("TWILIO_ALLOWED_MOBILE", "")
OTP_MODE = os.getenv("OTP_MODE", "twilio")

# Demo mode (OTP_MODE=demo) never contacts Twilio: it accepts this fixed
# 6-digit code instead. Useful for reviewers when no live SMS is desired.
OTP_DEMO_CODE = os.getenv("OTP_DEMO_CODE", "123456")


# ============================================================
# MEDIA FILES (Uploaded documents — never commit to Git)
# ============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# APPLICATION DEFINITION
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",

    "schemes",
    "accounts",
    "applications",
    "agent_api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    url = urllib.parse.urlparse(DATABASE_URL)
    engine = "django.db.backends.postgresql" if "postgres" in url.scheme else "django.db.backends.sqlite3"
    DATABASES = {
        "default": {
            "ENGINE": engine,
            "NAME": url.path.lstrip("/"),
            "USER": url.username or "",
            "PASSWORD": url.password or "",
            "HOST": url.hostname or "",
            "PORT": str(url.port or "5432"),
            "CONN_MAX_AGE": 600,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

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


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise serves compressed static files in production (DEBUG=False).
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# ============================================================
# EMAIL
# ============================================================

MAILERS = {
    "default": {
        "BACKEND": os.getenv(
            "DJANGO_EMAIL_BACKEND",
            "django.core.mail.backends.smtp.EmailBackend" if not DEBUG else "django.core.mail.backends.console.EmailBackend"
        ),
    },
}


# ============================================================
# REST FRAMEWORK & THROTTLING
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/min",
        "user": "300/min",
        "agent_api": "120/min",
        "agent_public": "300/min",
    },
}


# ============================================================
# SECURITY & COOKIES (Production HTTPS settings)
# ============================================================

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    if os.getenv("DJANGO_SECURE_SSL_REDIRECT", "True").lower() in ("true", "1", "yes"):
        SECURE_SSL_REDIRECT = True
