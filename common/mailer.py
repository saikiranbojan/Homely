from __future__ import absolute_import
from django.core.mail.message import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf import settings

def send_email(subject="Subj", message="message", recipient_list=['admin@domain.com'],
               fail_silently=True, auth_user=None, auth_password=None, connection=None,
               html_message=None, attachments=None):
    
    from_email = settings.EMAIL_FROM_ADDRESS
    # email = EmailMultiAlternatives(subject, message, from_email,recipient_list)
    kwargs = dict(
                  to=recipient_list,
                  from_email=from_email,
                  subject=subject,
                  body=html_message,
                  attachments=attachments,
    )
    message = EmailMultiAlternatives(**kwargs)
    if html_message:
        message.attach_alternative(html_message, 'text/html')
    message.send(fail_silently=False)
    return True

