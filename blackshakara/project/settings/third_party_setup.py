# REDIS CACHE SETTINGS
CACHES = {
    "default": {
        "BACKEND": config('CACHE_BACKEND', default="django_redis.cache.RedisCache"),  # type: ignore # noqa: F821
        "LOCATION": config('CACHE_LOCATION', default="redis://127.0.0.1:6379/1"),  # type: ignore # noqa: F821
        'TIMEOUT': 2592000,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

SWAGGER_SETTINGS = {'SECURITY_DEFINITIONS': {'Token': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}}}

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = config('CACHE_LOCATION', default="redis://127.0.0.1:6379/1"),  # type: ignore # noqa: F821
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
