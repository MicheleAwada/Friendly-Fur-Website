# Generated by Django 4.2.4 on 2023-08-25 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='productIngrediants',
            new_name='productIngredients',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='ingrediants',
            new_name='ingredients',
        ),
    ]
