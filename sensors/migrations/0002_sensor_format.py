# Generated by Django 3.1.4 on 2020-12-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='format',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
