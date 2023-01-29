from pathlib import Path
from os import environ as env
from kombu import Queue
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env["SECRET_KEY"]

DEBUG = env["DEBUG"]

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_elasticsearch_dsl",
    "src.pollution.apps.PollutionConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

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

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env["PG_HOST"],
        "PORT": env["PG_PORT"],
        "USER": env["PG_USER"],
        "PASSWORD": env["PG_PASSWORD"],
        "NAME": env["PG_DB"],
    }
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# RabbitMQ
RABBITMQ_USERNAME = env["RABBITMQ_USERNAME"]
RABBITMQ_PASSWORD = env["RABBITMQ_PASSWORD"]
RABBITMQ_HOST = env["RABBITMQ_HOST"]
RABBITMQ_PORT = env["RABBITMQ_PORT"]
RABBITMQ_VHOST = env["RABBITMQ_VHOST"]
RABBITMQ_DURABLE = True
RABBITMQ_EXCLUSIVE = False


# Celery
CELERY_BROKER_URL = env["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = env["CELERY_RESULT_BACKEND"]
CELERY_ACCEPT_CONTENT = ["application/json", "pickle"]
CELERY_RESULT_EXPIRES = env["CELERY_RESULT_EXPIRES"]
CELERY_TASK_EXPIRATION_TIME_IN_SECONDS = 120
CELERY_TASK_QUEUES = [
    Queue(name=q)
    for q in [
        "celery.queue.air.pollution",
    ]
]


# Elasticsearch
ELASTICSEARCH_DSL = {
    "default": {"hosts": 'elasticsearch'},
}

NUMBER_OF_SHARDS = 1
NUMBER_OF_REPLICAS = 1

ELASTICSEARCH_DSL_AUTOSYNC = True
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'django_elasticsearch_dsl.signals.RealTimeSignalProcessor'

# OPEN_WEATHER
OPEN_WEATHER_API_KEY = env["OPEN_WEATHER_API_KEY"]