# Generated by Django 4.2.4 on 2023-09-01 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_remove_aboutproduct_dimension_x_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='about_product',
            field=models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='shop.aboutproduct'),
        ),
    ]
