from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import *
from . import forms


class GenreYear:
    """ Class for get all genres and years which are based on our movies """
    """ 
    Some views are inherited from current class and in template,
    which are displayed by CBV, in django we cas use "view" variable to 
    use all fields and methods of current class-based view. So, we also can use 
    all methods of current "mixin" class.
    """

    def get_genres(self):
        """ Method to return the queryset of all genres """
        return Genre.objects.all()

    def get_years(self):
        """ Method to return the dictionary of all distinct years """
        return Movie.objects.filter(draft=False).values_list('year', flat=True).distinct().order_by('year')


class MoviesListView(GenreYear, ListView):
    """ ListView class to display all movies as list of data """

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    context_object_name = 'movies'
    template_name = 'movies/movies_list.html'

    # def get_context_data(self, *args, **kwargs):
    #     """ Method to config our page context data """
    #     # First get the base context with super:
    #     context = super().get_context_data(*args, **kwargs)
    #     # Second add categories as new context data (as new key in dictionary of page context):
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(GenreYear, DetailView):
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


class ActorDetailView(GenreYear, DetailView):
    """ DetailView class to display the information about one actor """

    model = Actor
    context_object_name = 'actor'
    template_name = 'movies/actor.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'


class FilterMoviesView(GenreYear, ListView):
    """ Class for filtering movies """
    model = Movie
    template_name = 'movies/movies_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        # Method GETLIST instead of get, we should use, when we want to get the list of elements.
        # If we try to use get-method to get list, we will see only the first element in collection!

        # Return queryset of movies where years and genres are checked by user in forms:
        return Movie.objects.filter(
            # With Q class we can combine different conditions (and=&, or=|, ...) for filtering and getting objects:
            Q(year__in=self.request.GET.getlist('year')) |      # Get the years list
            Q(genres__in=self.request.GET.getlist('genre'))   # Get the genres list
        ).order_by('year')  # Ordering films by year
