from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import *


# Create your views here.
# class MoviesView(View):
#     """View class for movies"""
#
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, template_name='movies/movies.html', context={'movies': movies})
#
#
# class MovieDetailView(View):
#     """ View class for one movie with its details"""
#
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, template_name='movies/movie_detail.html', context={'movie': movie})


class MoviesListView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    context_object_name = 'movies'
    template_name = 'movies/movies.html'


class MovieDetailView(DetailView):
    model = Movie
    # slug_field - its an attribute to specify the field name of our model which we use
    # instead default slug field in model
    slug_field = 'url'
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'
