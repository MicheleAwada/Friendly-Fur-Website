# Generated by Django 4.2.4 on 2023-08-25 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutproduct',
            name='Weight',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Product Weight in grams'),
        ),
    ]
