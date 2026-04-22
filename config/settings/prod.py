from .base import *  # noqa
from django.core.exceptions import ImproperlyConfigured

DEBUG = False

if not SECRET_KEY or SECRET_KEY in {"dev-secret-key-change-me", "change-me"}:
    raise ImproperlyConfigured("Set a real SECRET_KEY before starting production.")

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("Set ALLOWED_HOSTS for production deployment.")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = env_int("SECURE_HSTS_SECONDS", 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", False)
