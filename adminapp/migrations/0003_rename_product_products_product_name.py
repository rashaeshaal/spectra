# Generated by Django 4.2.3 on 2023-07-19 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_rename_product_name_products_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='product',
            new_name='product_name',
        ),
    ]
