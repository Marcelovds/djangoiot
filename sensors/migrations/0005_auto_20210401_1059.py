# Generated by Django 3.1.4 on 2021-04-01 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0004_auto_20210124_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='format',
            field=models.CharField(blank=True, help_text='Leave empty to use the default format for the sensor (recommended).', max_length=200),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='type',
            field=models.CharField(choices=[('temperature', 'Temperature and Humidity'), ('pressure', 'Atmospheric pressure'), ('luminance', 'Ambient luminance')], default='temperature', max_length=20),
        ),
    ]
