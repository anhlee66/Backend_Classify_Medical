# Generated by Django 3.2.5 on 2024-05-27 02:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_authentication', '0006_alter_log_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 9, 59, 29, 433928)),
        ),
    ]
