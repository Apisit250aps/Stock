# Generated by Django 5.0.1 on 2024-01-15 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_order_customer_order_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fax',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='tel',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
