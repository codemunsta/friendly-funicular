from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.schedules import crontab
# from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery('project')

app.conf.enable_utc = True

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {}

app.autodiscover_tasks()
