# Generated by Django 4.2.4 on 2023-09-02 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0034_rename_weight_aboutproduct_weight'),
        ('authe', '0005_customeruser_cart_alter_customeruser_dog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeruser',
            name='cart',
        ),
        migrations.CreateModel(
            name='CustomerCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_carts', to='shop.product', verbose_name='Users Cart')),
            ],
        ),
        migrations.AddField(
            model_name='customeruser',
            name='user_cart',
            field=models.ManyToManyField(blank=True, related_name='all_carts_inside', to='authe.customercart', verbose_name='Users Cart'),
        ),
    ]
