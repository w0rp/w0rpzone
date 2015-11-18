from settings_base import *  # nopep8

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS = (
    ("test-admin", "test@fake.com"),
)

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SECRET_KEY = "thisisntverysecretnowisit?"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/dev/shm/w0rpzone.db",
        "TEST": {
            "CHARSET": "UTF8",
            "NAME": None,
        }
    }
}
