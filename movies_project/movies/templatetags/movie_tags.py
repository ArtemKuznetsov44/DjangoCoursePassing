from django import template
from movies.models import Category, Movie

# Create the instance of Library to register our tags:
register = template.Library()


@register.simple_tag()
def get_categories():
    """ Current simple tag is used to get all categories """
    return Category.objects.all()


@register.inclusion_tag(filename='movies/tags/last_movies.html')
def get_last_movie_additions(count: int = 5):
    # Get the queryset of Movie objects which are ordered by id in desc:
    last_additions = Movie.objects.order_by('-id')[:count]
    return {'last_additions': last_additions}
