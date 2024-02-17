from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from .models import *
from . import forms


# Create your views here.
# class MoviesView(View):
#     """View class for movies"""
#
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, template_name='movies/movies_list.html', context={'movies': movies})
#
#
# class MovieDetailView(View):
#     """ View class for one movie with its details"""
#
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, template_name='movies/movie_detail.html', context={'movie': movie})


class MoviesListView(ListView):
    """ ListView class to display all movies as list of data """

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    context_object_name = 'movies'
    template_name = 'movies/movies_list.html'


class MovieDetailView(DetailView):
    """ DetailView class for display one movie with details """

    model = Movie
    # slug_field - its an attribute to specify the field name of our model which we use
    # instead default slug field in model
    slug_field = 'url'
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'


class AddReview(View):
    """ View class to add reviews with form to create new review """

    def post(self, request, pk):
        # With such code we get data from request.POST dictionary into our form and fill our form.
        # With form, we can check that data is valid
        form = forms.AddReviewForm(request.POST)
        movie = Movie.objects.get(pk=pk)

        # Check that form is valid:
        if form.is_valid():

            # When we call save in model form object without commit=False param, our object will save in db,
            # but in our case we stop this event, because we need to add the movie pk to save our Review.
            # Our form does not contain such field to get pk of movie from user, but our Review model
            # contains such field.
            # So we need to add to form movie by hands/
            form = form.save(commit=False)

            # In our post request we try to find parent
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))

            # form.movie need to get Movie model object but with from.movie_id construction we can use only integer pk
            # value and django will use this value to make relationship for ForeignKeyField
            # More that, movie_id it is a column name in db table for Reviews.
            # without needs to get Movie object.
            form.movie = movie
            # We use ModelForm class - so form.save() command will create new object in our db.
            form.save()

        return redirect(movie.get_absolute_url())
