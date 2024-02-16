from django.contrib import admin
from .models import *


# Register your models here.
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Actor)
# class ActorAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Genre)
# class GenreAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Movie)
# class MovieAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(MovieShorts)
# class MovieShortsAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(RatingStar)
# class RatingStarAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Reviews)
# class ReviewsAdmin(admin.ModelAdmin):
#     pass


# Just for compare:
admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShorts)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Reviews)

