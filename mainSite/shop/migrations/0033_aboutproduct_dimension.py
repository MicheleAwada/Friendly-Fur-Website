# Generated by Django 4.2.4 on 2023-09-01 13:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_remove_aboutproduct_dimension_product_about_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutproduct',
            name='dimension',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=3, max_digits=10), blank=True, null=True, size=3),
        ),
    ]
