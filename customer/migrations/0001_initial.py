# Generated by Django 5.0.1 on 2024-01-13 03:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('contact', models.CharField(blank=True, max_length=255)),
                ('tel', models.CharField(blank=True, max_length=10)),
                ('fax', models.CharField(blank=True, max_length=10)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('remark', models.TextField(blank=True)),
                ('province', models.CharField(blank=True, max_length=255)),
                ('district', models.CharField(blank=True, max_length=255)),
                ('sub_district', models.CharField(blank=True, max_length=255)),
                ('address', models.TextField(blank=True, null=True)),
                ('zip', models.CharField(blank=True, max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
