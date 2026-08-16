from django.urls import path
from .views import MovieListCreateView

urlpatterns = [
    path("", MovieListCreateView.as_view(), name="movie-list-create"),
    path("<uuid:movie_id>/", MovieListCreateView.as_view(), name="movie-update"),
    path("<uuid:movie_id>/", MovieListCreateView.as_view(), name="movie-delete")
]