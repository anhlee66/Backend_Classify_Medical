# Generated by Django 5.0.6 on 2024-06-23 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_authentication', '0009_alter_log_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 19, 6, 42, 816822)),
        ),
    ]
