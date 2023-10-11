from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(subject: str, template: str, to_email: str|list, context: dict, request=None) -> int:
    html_message = render_to_string(template_name=template, context=context, request=request)

    try:
        email_sent = EmailMultiAlternatives(subject=subject, body=f"{settings.PROJECT_USER_READABLE_NAME} Email Notification", to=[to_email] if isinstance(to_email, str) else to_email)
        email_sent.attach_alternative(html_message, 'text/html')
        email_sent = email_sent.send()
    except Exception as e:
        raise e
        email_sent = 0
    
    return email_sent