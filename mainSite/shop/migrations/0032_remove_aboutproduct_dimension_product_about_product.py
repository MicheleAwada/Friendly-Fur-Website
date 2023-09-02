# Generated by Django 4.2.4 on 2023-09-01 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_remove_product_about_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutproduct',
            name='dimension',
        ),
        migrations.AddField(
            model_name='product',
            name='about_product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.aboutproduct'),
        ),
    ]
