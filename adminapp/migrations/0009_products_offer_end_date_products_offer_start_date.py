# Generated by Django 4.2.3 on 2023-08-17 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0008_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='offer_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='offer_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
