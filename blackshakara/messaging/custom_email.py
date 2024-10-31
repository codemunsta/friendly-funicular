from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_mail(subject, email, message):
    subject = subject
    msg1 = EmailMessage(subject, message, settings.DEFAULT_MAIL_SENDER, [email])
    msg1.send()


def send_html_email(subject, html_template_name, text_template_name, context, email):
    subject = subject
    html_content = render_to_string(html_template_name, context)
    text_content = render_to_string(text_template_name, context)

    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=settings.DEFAULT_MAIL_SENDER, to=[
        email,
    ])
    try:
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(e)


def send_bulk_html_email(subject, html_template_name, text_template_name, context, email):
    subject = subject
    html_content = render_to_string(html_template_name, context)
    text_content = render_to_string(text_template_name, context)

    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=settings.DEFAULT_MAIL_SENDER, to=email)
    email.attach_alternative(html_content, "text/html")
    email.send()
