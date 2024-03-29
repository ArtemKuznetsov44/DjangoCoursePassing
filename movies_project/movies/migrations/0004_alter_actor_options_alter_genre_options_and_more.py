# Generated by Django 5.0.2 on 2024-02-15 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_category_options_alter_movieshorts_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'verbose_name': 'Actor', 'verbose_name_plural': 'Actors'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Genre', 'verbose_name_plural': 'Genres'},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'verbose_name': 'Movie', 'verbose_name_plural': 'Movies'},
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Rating', 'verbose_name_plural': 'Ratings'},
        ),
    ]
