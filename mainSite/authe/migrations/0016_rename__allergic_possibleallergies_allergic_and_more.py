# Generated by Django 4.2.4 on 2023-09-12 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0015_possibleallergies__allergic_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='possibleallergies',
            old_name='_allergic',
            new_name='allergic',
        ),
        migrations.RenameField(
            model_name='possibleallergies',
            old_name='_dog_name',
            new_name='dog_name',
        ),
    ]
