# Generated by Django 4.2.4 on 2023-08-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_aboutproduct_weight_alter_colors_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sizes',
            name='Dimensionx',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sizes',
            name='Dimensiony',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sizes',
            name='Dimensionz',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sizes',
            name='size_name',
            field=models.CharField(blank=True, default='default', max_length=30),
        ),
    ]
