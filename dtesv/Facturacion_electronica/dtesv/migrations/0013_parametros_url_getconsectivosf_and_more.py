# Generated by Django 4.1.13 on 2024-01-19 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtesv', '0012_documentos_anuladoerp'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametros',
            name='url_getconsectivoSF',
            field=models.CharField(default='http://192.168.1.53:5010/api/consecutivos/', max_length=255),
        ),
        migrations.AddField(
            model_name='parametros',
            name='url_setconsectivoSF',
            field=models.CharField(default='http://192.168.1.53:5010/api/consecutivosUp/', max_length=255),
        ),
    ]
