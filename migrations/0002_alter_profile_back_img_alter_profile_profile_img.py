# Generated by Django 4.2.3 on 2023-07-25 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opanahub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='back_img',
            field=models.ImageField(default='img/thin.jpg', upload_to='back_images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='img/blank.webp', upload_to='profile_images'),
        ),
    ]
