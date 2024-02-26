from django.shortcuts import render, redirect, HttpResponse
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
    # queryset = Movie.objects.filter(draft=False)
    context_object_name = 'movies'
    template_name = 'movies/movies_list.html'

    # TODO: Add button to clear all filters!
    def get_queryset(self):
        """ Method to return the queryset of all movies and with filters """

        # Making the default queryset for current method:
        base_queryset = Movie.objects.filter(draft=False)

        # In current block we try to get arrays with years and genres:
        years = self.request.GET.getlist('year', None)
        genres = self.request.GET.getlist('genre', None)

        # Make some checks to and filter our default queryset if it needs:
        if years and not genres:
            return base_queryset.filter(year__in=years)
        elif genres and not years:
            return base_queryset.filter(genres__in=genres)
        elif genres and years:
            return base_queryset.filter(year__in=years, genres__in=genres)

        # If no event in if-block, return the default queryset:
        return base_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = [*map(int, self.request.GET.getlist('year', None))]
        context['genres'] = [*map(int, self.request.GET.getlist('genre', None))]
        return context


class MovieDetailView(GenreYear, DetailView):
    """ DetailView class for display one movie with details """

    model = Movie
    # slug_field - it's an attribute to specify the field name of our model which we use
    # instead default slug field in model
    slug_field = 'url'
    context_object_name = 'movie'
    template_name = 'movies/movie_detail.html'

    def get_context_data(self, **kwargs):
        """
        Current method can be useful when we need to add more context into view.
        Here we add our form to add rating star for movie
        """

        context = super().get_context_data(**kwargs)
        # Create new instance of RatingForm and add it to the page context:
        context['rating_form'] = forms.RatingForm()
        return context


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


class AddStarRatingView(View):
    """ Class view to add rating star to the movie """

    def get_client_ip(self, request):
        """ Method to get the user ip address from http request """

        # Usually the info about user ip go through the header HTTP_X_FORWARDED_FOR:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # If it is:
        if x_forwarded_for:
            # It can contain more than one ip if current request when through not one proxy, so
            # to get the user ip we need takes the first one:
            ip = x_forwarded_for.split(',')[0]
        else:
            # If request does not contain the HTTP_X_FORWARDED_FOR header,
            # we get the ip from directly from the variable 'REMOTE_ADDR':
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def post(self, request):
        """ In current post method we work with post-request by user """

        # Getting form data from request.POST into our form for then validation:
        form = forms.RatingForm(request.POST)
        # Validation:
        if form.is_valid():
            # update_or_create method we can use when we do not know, has db such ratings by current user or not
            # So if he has, we update it, if he has not, create:
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                # defaults - it is not the field name, but we need to use it, because of update_or_create method.
                # It means, that we need to specify the dictionary of {'db_column_name': value}. Current dictionary
                # django will use to know what he needs to update and how if hase already exist in db:
                defaults={'star_id': int(request.POST.get('star'))}
            )

            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
