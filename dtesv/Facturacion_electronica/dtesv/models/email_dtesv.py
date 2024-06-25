from django.db import models

class EmailConfig(models.Model):
    email_host = models.CharField(max_length=255)
    email_port = models.IntegerField()
    email_use_tls = models.BooleanField(default=True)
    email_host_user = models.CharField(max_length=255)
    email_host_password = models.CharField(max_length=255)
    default_from_email = models.CharField(max_length=255)

    def __str__(self):
        return self.email_host_user