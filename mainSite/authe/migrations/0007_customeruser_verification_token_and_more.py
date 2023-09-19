# Generated by Django 4.2.4 on 2023-09-06 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0006_remove_customeruser_cart_customercart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeruser',
            name='verification_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customeruser',
            name='verification_token_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
