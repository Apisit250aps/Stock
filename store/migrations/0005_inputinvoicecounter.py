# Generated by Django 4.2.6 on 2024-01-04 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_inputinvoice_remark_alter_shop_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputInvoiceCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_date', models.CharField(max_length=6)),
                ('no', models.IntegerField(default=0)),
            ],
        ),
    ]