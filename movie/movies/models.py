from django.db import models
import uuid

class Status(models.TextChoices):
    UPCOMING = "UPCOMING", "Upcoming"
    RELEASED = "RELEASED", "Released"
    ENDED = "ENDED", "Ended"



#genre model
class Genre(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        db_table = "genre"
        ordering = ["-name"]


#Movie model
class Movie(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(
        max_length=200,
        db_index=True
    )

    description = models.TextField(
        blank=True
    )

    duration_minutes = models.PositiveSmallIntegerField()

    release_date = models.DateField(
        db_index=True
    )

    language = models.CharField(
        max_length=50,
        db_index=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING,
        db_index=True
    )

    genre = models.ManyToManyField(
        Genre,
        through="MovieGenre",
        related_name="movies"
    )

    class Meta:
        db_table = "movies"
        ordering = ["-release_date"]

        def __str__(self):
            return self.title



#movie-genre model
class MovieGenre(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_genre"
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="movie_genres"
    )

    class Meta:
        db_table = "movie_genres"

        def __str__(self):
            return f"{self.movie.title} - {self.genre.name}"