# Generated by Django 5.0.6 on 2024-07-31 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rova', '0004_volunteer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
