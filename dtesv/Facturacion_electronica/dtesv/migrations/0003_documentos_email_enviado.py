# Generated by Django 4.1.9 on 2023-10-02 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtesv', '0002_alter_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentos',
            name='email_enviado',
            field=models.BooleanField(db_column='email_enviado', default=False),
        ),
    ]
