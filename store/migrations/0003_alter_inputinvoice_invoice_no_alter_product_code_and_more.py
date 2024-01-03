# Generated by Django 4.2.6 on 2024-01-03 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_shop_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputinvoice',
            name='invoice_no',
            field=models.CharField(max_length=16, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=8, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='code',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]