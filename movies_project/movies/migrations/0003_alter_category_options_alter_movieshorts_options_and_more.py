# Generated by Django 5.0.2 on 2024-02-15 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='movieshorts',
            options={'verbose_name': 'MovieShort', 'verbose_name_plural': 'MovieShorts'},
        ),
        migrations.AlterModelOptions(
            name='ratingstar',
            options={'verbose_name': 'RatingStar', 'verbose_name_plural': 'RatingStars'},
        ),
        migrations.AlterModelOptions(
            name='reviews',
            options={'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
    ]
