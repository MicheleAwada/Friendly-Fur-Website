# Generated by Django 4.2.4 on 2023-09-17 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_remove_product_dog_allergic_name'),
        ('authe', '0020_possibleallergies_allergic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='possibleallergies',
            name='allergic',
        ),
        migrations.RemoveField(
            model_name='unverifieduser',
            name='userid',
        ),
        migrations.AddField(
            model_name='unverifieduser',
            name='verf_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Unverified_Email_Change', to=settings.AUTH_USER_MODEL, verbose_name='Verified_Users_Email_Change'),
        ),
        migrations.AlterField(
            model_name='customercart',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='in_carts', to='shop.product', verbose_name='Users Cart'),
        ),
    ]
