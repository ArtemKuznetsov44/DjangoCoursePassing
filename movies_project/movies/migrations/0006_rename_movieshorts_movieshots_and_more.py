# Generated by Django 5.0.2 on 2024-02-17 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_movieshorts_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MovieShorts',
            new_name='MovieShots',
        ),
        migrations.AlterModelOptions(
            name='movieshots',
            options={'verbose_name': 'MovieShot', 'verbose_name_plural': 'MovieShots'},
        ),
    ]