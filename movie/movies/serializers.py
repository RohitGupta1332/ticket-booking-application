from rest_framework import serializers

from .models import Genre, Movie, MovieGenre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre

        fields = [
            "id",
            "name"
        ]


class MovieListSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "duration_minutes",
            "release_date",
            "language",
            "status",
            "genre"
        ]

class MovieCreateSerializer(serializers.ModelSerializer):

    genre_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        source="genre"
    )

    class Meta:
        model = Movie

        fields = [
            "title",
            "description",
            "duration_minutes",
            "release_date",
            "language",
            "status",
            "genre_ids"
        ]

    def create(self, validated_data):
        genres = validated_data.pop("genre", [])
        movie = Movie.objects.create(**validated_data)
        for genre in genres:
            MovieGenre.objects.create(movie=movie, genre=genre)
        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop("genre", [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # reset genres
        MovieGenre.objects.filter(movie=instance).delete()
        for genre in genres:
            MovieGenre.objects.create(movie=instance, genre=genre)
        return instance