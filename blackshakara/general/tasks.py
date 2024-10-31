from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.contrib.auth import get_user_model

from ..messaging.custom_email import send_html_email

User = get_user_model()


@shared_task
def send_email_tasks(subject, html, text, context, email):
    send_html_email(subject, html, text, context, email)
    return True
