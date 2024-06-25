# dtesv/utils.py

from django.core.mail import EmailMultiAlternatives
from dtesv.dtesv_email_settings import get_email_backend
from dtesv.models import EmailConfig

def enviar_correo_con_adjuntos(subject, message, recipient_list, attachments, html_message=None):
    email_backend = get_email_backend()
    config = EmailConfig.objects.first()

    email = EmailMultiAlternatives(
        subject,
        message,
        config.default_from_email,
        recipient_list,
        connection=email_backend
    )

    if html_message:
        email.attach_alternative(html_message, "text/html")

    # Agregar los archivos adjuntos
    for attachment in attachments:
        email.attach(attachment['filename'], attachment['content'], attachment['mimetype'])

    value = email.send()
    return value
