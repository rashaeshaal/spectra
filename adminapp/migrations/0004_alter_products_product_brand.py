# Generated by Django 4.2.3 on 2023-07-21 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_rename_product_products_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.brands'),
        ),
    ]