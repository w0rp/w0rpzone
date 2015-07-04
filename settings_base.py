# Django settings for w0rpzone project.

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PIPELINE_ENABLED = True

PROJECT_ROOT = os.path.dirname(__file__)

ADMINS = ()
MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Being in INTERNAL_IPS enables the debug flag for templates.
# This turns non-minified JS on, etc.
INTERNAL_IPS = (
    "127.0.0.1",
)

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static/")

STATIC_URL = "/static/"

STATICFILES_DIRS = (
    "staticfiles",
)

ADMIN_REGEX = r"^admin/"
LOGIN_REGEX = r"^login/$"
LOGIN_URL = "/login/"
LOGOUT_REGEX = r"^logout/$"
LOGOUT_URL = "/logout/"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Use the cached template loader for Django templates.
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [os.path.join(PROJECT_ROOT, "template")],
    "OPTIONS": {
        "loaders": [
            ("django.template.loaders.cached.Loader", [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ]),
        ],
        "context_processors": (
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.core.context_processors.tz",
            "django.contrib.messages.context_processors.messages",
            "django.core.context_processors.request",
            "misc.context_processors.navigation",
        ),
    },
}]

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "pipeline.middleware.MinifyHTMLMiddleware",
    "misc.middleware.LocaleMiddleware",
)

ROOT_URLCONF = "urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "wsgi.application"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Enable Django admin.
    "django.contrib.admin",
    # Enable admin docs.
    "django.contrib.admindocs",
    "gunicorn",
    "pipeline",
    "w0rplib",
    "misc",
    "blog",
    "programming_projects",
)

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        "syslog": {
            "address": "/dev/log",
            "class": "logging.handlers.SysLogHandler"
        }
    },
    'loggers': {
        "": {
            'handlers': ["syslog"],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

TEST_RUNNER = "django.test.runner.DiscoverRunner"

# django-pipeline settings

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

# Disable JavaScript wrapping. Just copy it across.
PIPELINE_DISABLE_WRAPPER = True

# Use the versioned cached storage for cache killing.
STATICFILES_STORAGE = "pipeline.storage.PipelineCachedStorage"

# Use pipeline for finding files.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
    "pipeline.finders.CachedFileFinder",
)

PIPELINE_CSS = {
    "main-site": {
        "source_filenames": (
            "css/droidsans.css",
            "css/source_code_pro.css",
            "css/highlight_obsidian.css",
            "css/base.css",
            "css/blog/main.css",
            "css/blog/public.css",
            "css/blog/edit.css",
        ),
        "output_filename": "css/combined.css"
    },
}

PIPELINE_CSS_COMPRESSOR = "w0rplib.compiler.CSSCompressor"

PIPELINE_JS = {
    "main-site": {
        "source_filenames": (
            "js/jquery-2.0.3.min.js",
            "js/jstz.min.js",
            "js/notify-combined.min.js",
            "js/jquery.cookie.js",
            "js/highlight.pack.js",
            "js/soverflow_like_highlight.js",
            "js/marked.js",
            "js/global.js",
            "js/blog/main.js",
            "js/blog/edit.js",
            "js/blog/comment.js",
        ),
        "output_filename": "css/combined.js"
    },
}

PIPELINE_JS_COMPRESSOR = "w0rplib.compiler.RJSMinCompressor"

DDOC_TEMPLATE = "programming_projects/doc.ddoc"

NO_REPLY_EMAIL = "no-reply@w0rp.com"
EXTERNAL_SITE_URL = "https://w0rp.com"
