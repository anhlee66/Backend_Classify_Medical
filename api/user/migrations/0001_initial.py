# Generated by Django 5.0.6 on 2024-06-22 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'departments',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('gender', models.BooleanField(default=True)),
                ('permission', models.CharField(choices=[('ADMIN', 'admin'), ('STUDENT', 'student'), ('OFFICER', 'officer')], default='student', max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created', models.DateField(auto_now_add=True)),
                ('avatar', models.CharField(default='default.jpg', max_length=255)),
                ('department', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_user.department')),
            ],
        ),
    ]
