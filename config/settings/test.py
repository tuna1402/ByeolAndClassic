from .base import *  # noqa

DEBUG = False
SECRET_KEY = "test-secret-key"
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# 테스트는 빠르게: 비밀번호 해시 최소화
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
