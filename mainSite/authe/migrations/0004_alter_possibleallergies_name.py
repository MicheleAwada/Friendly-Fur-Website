# Generated by Django 4.2.4 on 2023-08-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0003_customeruser_dog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='possibleallergies',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
