# Generated by Django 4.2.3 on 2023-08-09 05:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminapp', '0007_alter_products_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField()),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('amount', 'Amount')], max_length=10)),
                ('discount', models.DecimalField(decimal_places=0, max_digits=10)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('applicable_type', models.CharField(choices=[('all', 'Category All'), ('category', 'Category')], max_length=10)),
                ('min_purchase', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('max_amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True)),
                ('usage_limit', models.PositiveIntegerField(default=0)),
                ('times_used', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.category')),
            ],
        ),
    ]
