# Generated by Django 5.0.6 on 2024-07-25 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rova', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
