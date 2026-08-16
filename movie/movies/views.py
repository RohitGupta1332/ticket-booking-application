from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Movie
from .serializers import MovieListSerializer, MovieCreateSerializer
from .service import MovieService


class MovieListCreateView(APIView):

    def get(self, request):

        movies = Movie.objects.prefetch_related("genre").all()

        serailizers = MovieListSerializer(movies, many=True)

        return Response({
            "response": serailizers.data
        }, status=status.HTTP_200_OK)


    def post(self, request):

        serializer = MovieCreateSerializer(data=request.data)

        if serializer.is_valid():
            try:
                movie = MovieService.create_movie(serializer.validated_data)
                response_serializer = MovieListSerializer(movie)
    
                return Response({
                    "response": response_serializer.data
                },
                status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, movie_id):

        try:
            movie = Movie.objects.filter(id=movie_id).first()

            if movie is None:
                return Response(
                    {
                        "detail": "Movie not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            movie.delete()
            return Response({
                "detail": "Movie deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            )

    def put(self, request, movie_id):

        try:
            movie = Movie.objects.filter(id=movie_id).first()
            if movie is None:
                return Response(
                    {
                        "detail": "Movie not found"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            serializer = MovieCreateSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "detail": "Movie updated successfully"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "detail": serializer.errors
                }, status= status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    




