# Generated by Django 3.2.5 on 2024-05-27 03:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_label', '0030_alter_model_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 10, 2, 36, 186907)),
        ),
    ]
