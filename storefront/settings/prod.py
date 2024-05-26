import os
from .common import *
import dj_database_url


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['storefrontrestapi.onrender.com']

DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://devsearchuser:{DATABASE_PASSWORD}@dpg-co7eu3ev3ddc739568ig-a:5432/storefront',
        conn_max_age=600
    )
}

CELERY_BROKER_URL = os.environ.get('redis-cache-broker')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('redis-cache-broker'),
        "TIMEOUT": 10*60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}