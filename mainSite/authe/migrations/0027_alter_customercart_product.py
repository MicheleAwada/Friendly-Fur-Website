# Generated by Django 4.2.4 on 2023-10-19 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0039_productimages_descaled_image_alter_brand_slug_and_more'),
        ('authe', '0026_alter_possibleallergies_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_carts', to='shop.product', verbose_name='Users Cart'),
        ),
    ]
