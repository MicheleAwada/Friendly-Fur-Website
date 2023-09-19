# Generated by Django 4.2.4 on 2023-09-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0022_customerdog_dog_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='PossibleBreeds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('color', models.CharField(blank=True, max_length=7, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='customerdog',
            name='dog_number',
            field=models.PositiveIntegerField(),
        ),
    ]
