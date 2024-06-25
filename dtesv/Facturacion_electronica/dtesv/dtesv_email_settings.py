# dtesv/email_settings.py

from django.core.mail import get_connection
from .models import EmailConfig

def get_email_backend():
    config = EmailConfig.objects.first()
    if not config:
        raise Exception("Configura la configuración de correo electrónico en el admin de Django.")
    
    email_backend = get_connection(
        host=config.email_host,
        port=config.email_port,
        username=config.email_host_user,
        password=config.email_host_password,
        use_tls=config.email_use_tls
    )
    return email_backend
