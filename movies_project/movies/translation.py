from modeltranslation.translator import register, TranslationOptions
from .models import Category, Actor, Movie, Genre, MovieShots

"""
In current file we can register our models with modeltranslation app with translator
Then, under the classes description we can specify fields which could be translated. 
After registration, we need to make new migration and make them. 
All specify fields here will have their copies in database but with locale specification. 
"""


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(MovieShots)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
