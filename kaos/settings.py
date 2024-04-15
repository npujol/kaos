from pathlib import Path

import environ
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(overrides=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="a_valid_key")  # type: ignore

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"] if not DEBUG else ["*"]

# Application definition
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "debug_toolbar",
    "anki",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "kaos.urls"
LOGIN_URL = "admin:login"

LOGIN_REDIRECT_URL = reverse_lazy("admin:index")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kaos.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

main_database = env.db(
    "DB_URL",
    default="psql://postgres:postgres@localhost:5433/ankidb",  # type: ignore
)

main_database["CONN_MAX_AGE"] = 60  # type: ignore
main_database["DISABLE_SERVER_SIDE_CURSORS"] = True  # type: ignore
main_database["CONN_HEALTH_CHECKS"] = True  # type: ignore

DATABASES = {"default": main_database}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "::1",
    # ...
]
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

ROOT_URLCONF = "kaos.urls"

######################################################################
# Static
######################################################################

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_URL = "django-static/"
STATIC_ROOT = BASE_DIR / "static"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

UNFOLD = {
    "SITE_HEADER": _("Kaos Admin"),
    "SITE_TITLE": _("Kaos Admin"),
    "SITE_SYMBOL": "settings",
    "SHOW_HISTORY": True,
    "ENVIRONMENT": "kaos.utils.environment_callback",
    "DASHBOARD_CALLBACK": "anki.views.dashboard_callback",
    "LOGIN": {
        "image": lambda request: static("images/login-bg.jpg"),
    },
    "TABS": [
        {
            "models": [
                "anki.ankicards",
            ],
            "items": [
                {
                    "title": _("Anki Cards"),
                    "icon": "sports_motorsports",
                    "link": lambda request: reverse_lazy(
                        "admin:anki_ankicard_changelist"
                    ),
                },
            ],
        },
        {
            "models": [
                "django_celery_beat.clockedschedule",
                "django_celery_beat.crontabschedule",
                "django_celery_beat.intervalschedule",
                "django_celery_beat.periodictask",
                "django_celery_beat.solarschedule",
            ],
            "items": [
                {
                    "title": _("Tasks"),
                    "icon": "task_alt",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_clockedschedule_changelist"
                    ),
                },
                {
                    "title": _("Intervals"),
                    "icon": "arrow_range",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_intervalschedule_changelist"
                    ),
                },
                {
                    "title": _("Periodic tasks"),
                    "icon": "task",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_periodictask_changelist"
                    ),
                },
                {
                    "title": _("Solar events"),
                    "icon": "event",
                    "link": reverse_lazy(
                        "admin:django_celery_beat_solarschedule_changelist"
                    ),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Anki Cards"),
                        "icon": "sports_motorsports",
                        "link": lambda request: reverse_lazy(
                            "admin:anki_ankicard_changelist"
                        ),
                    },
                ],
            },
            {
                "separator": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:anki_ankiuser_changelist"),
                    },
                    {
                        "title": _("Tasks"),
                        "icon": "task_alt",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_clockedschedule_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}


# Celery
CELERY_BROKER_URL = env("CELERY_REDIS_URL", default="a_valid_key")  # type: ignore
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_IGNORE_RESULT = True
CELERY_RESULT_SERIALIZER = "json"
