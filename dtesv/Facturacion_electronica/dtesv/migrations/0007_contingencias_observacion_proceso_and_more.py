# Generated by Django 4.1.13 on 2023-12-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtesv', '0006_documentos_selloinvalidacion_alter_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='contingencias',
            name='observacion_proceso',
            field=models.TextField(blank=True, db_column='observaciones_proceso', null=True),
        ),
        migrations.AddField(
            model_name='contingencias',
            name='observaciones_mh',
            field=models.TextField(blank=True, db_column='observaciones_mh', null=True),
        ),
    ]