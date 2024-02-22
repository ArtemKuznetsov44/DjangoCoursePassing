from django.urls import path
from . import views

urlpatterns = [
    path('', views.MoviesListView.as_view(), name='movies'),
    path('filter/', views.FilterMoviesView.as_view(), name='filter_movies'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:name>/', views.ActorDetailView.as_view(), name='actor_detail'),


]