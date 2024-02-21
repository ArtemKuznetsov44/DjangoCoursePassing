import datetime
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Category Model"""
    name = models.CharField(max_length=150)
    description = models.TextField()
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        """
        Method to configure the object string representation as category name
        :return: String with category name
        """
        return self.name

    class Meta:
        # Specify the verbose_name field because by default django use first letter in lower case:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Actor(models.Model):
    """Actor Model"""
    name = models.CharField(max_length=100)
    # PositiveSmallIntegerField - it is a type for integer values from 0 to 32767
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='actors/')

    def __str__(self):
        """
        Method to configure the object string representation as actor name
        :return: String with actor name
        """

        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'name': self.name})

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'




class Genre(models.Model):
    """Genre Model"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        """
        Method to configure the object string representation as genre name
        :return: String with genre name
        """

        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    """Movie Model"""
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100, default='')
    description = models.TextField()
    poster = models.ImageField(upload_to="movies/")
    year = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=30)
    directors = models.ManyToManyField(to='Actor', related_name='movie_director')
    actors = models.ManyToManyField(to='Actor', related_name='movie_actor')
    genres = models.ManyToManyField(to='Genre', related_name='movie_genre')
    world_premier = models.DateField(default=datetime.date.today)
    budget = models.PositiveIntegerField(default=0, help_text='Specify the budget in dollars')
    fees_in_usa = models.PositiveIntegerField(default=0, help_text='Specify the fees in dollars')
    fees_in_world = models.PositiveIntegerField(default=0, help_text='Specify the fees in dollars')
    # on_delete=models.SET_NULL - that's mean that when we delete related category this field for movie will become NULL
    category = models.ForeignKey(to='Category', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        """
        Method to configure the object string representation as movie title
        :return: String with movie title
        """

        return self.title

    def get_absolute_url(self):
        # The REVERSE method will configurate the url by its name and specified in kwargs dictionary params:
        return reverse('movie_detail', kwargs={'slug': self.url})

    #
    def get_review(self):
        """
        This method will return our reviews for current movie object where parent of review will be null
        :return: Reviews with null parent
        """
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MovieShots(models.Model):
    """Movie Shorts Model"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='movie_shots/', null=True)
    # on_delete=models.CASCADE - that's mean that when we will delete movie all related movie short will be deleted
    movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE)

    def __str__(self):
        """
        Method to configure the object string representation as movie short title
        :return: String with movie short title
        """

        return self.title

    class Meta:
        verbose_name = 'MovieShot'
        verbose_name_plural = 'MovieShots'


class RatingStar(models.Model):
    """Rating Star Model"""
    value = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'RatingStar'
        verbose_name_plural = 'RatingStars'


class Rating(models.Model):
    """Rating Model"""
    ip = models.CharField(max_length=15)
    star = models.ForeignKey(to='RatingStar', on_delete=models.CASCADE)
    movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE)

    def __str__(self):
        """
        Method to configure the object representation as star value - movie
        :return:
        """

        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Reviews(models.Model):
    """Reviews Model"""
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    parent = models.ForeignKey(to='Reviews', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE)

    def __str__(self):
        """
        Method to configure the object representation as reviewer name and his or her email address
        :return: String with reviewer and name and his or her email address
        """

        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

