from django.db import transaction
from .models import Movie, MovieGenre

class MovieService:

    @staticmethod
    @transaction.atomic
    def create_movie(data):

        genres = data.pop("genre", [])

        movie = Movie.objects.create(**data)

        for genre in genres:
            MovieGenre.objects.create(movie=movie, genre=genre)

        return movie
