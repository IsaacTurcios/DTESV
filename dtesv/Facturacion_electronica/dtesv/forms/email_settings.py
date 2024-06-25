# dtesv/forms.py

from django import forms
from dtesv.models import EmailConfig

class EmailConfigForm(forms.ModelForm):
    class Meta:
        model = EmailConfig
        fields = '__all__'
        widgets = {
            'email_host_password': forms.PasswordInput(render_value=True),  # render_value=True para mostrar el valor actual
        }

    def clean(self):
        cleaned_data = super().clean()
        email_host = cleaned_data.get("email_host")
        email_port = cleaned_data.get("email_port")
        email_use_tls = cleaned_data.get("email_use_tls")
        email_host_user = cleaned_data.get("email_host_user")
        email_host_password = cleaned_data.get("email_host_password")

        # Intentar enviar un correo de prueba
        from django.core.mail import get_connection, EmailMessage
        try:
            connection = get_connection(
                host=email_host,
                port=email_port,
                username=email_host_user,
                password=email_host_password,
                use_tls=email_use_tls
            )
            email = EmailMessage(
                'Correo de prueba',
                'Este es un correo de prueba para validar la configuración.',
                email_host_user,
                [email_host_user],
                connection=connection
            )
            email.send()
        except Exception as e:
            raise forms.ValidationError(f"Error en la configuración de correo: {e}")

        return cleaned_data
