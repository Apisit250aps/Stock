# Generated by Django 5.0.1 on 2024-01-15 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_shop_email_alter_shop_fax_alter_shop_tel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='shop',
            name='fax',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='shop',
            name='tel',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
