# Generated by Django 3.2.5 on 2024-05-26 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_label', '0019_alter_model_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='created',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 26, 23, 10, 39, 375748)),
        ),
    ]
