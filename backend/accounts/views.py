from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import (
    RegisterSerializer,
    FavoriteMovieSerializer,
    WatchedMovieSerializer
)

from .models import (
    FavoriteMovie,
    WatchedMovie
)

# =========================
# REGISTER USER
# =========================

@api_view(['POST'])
def register_user(request):

    serializer = RegisterSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            {
                "message": "User created successfully"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# =========================
# ADD FAVORITE MOVIE
# =========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_favorite(request):

    data = request.data

    existing_favorite = FavoriteMovie.objects.filter(

        user=request.user,

        movie_title=data['movie_title']

    ).first()

    if existing_favorite:

        return Response({

            "message": "Already favorited"

        })

    favorite = FavoriteMovie.objects.create(

        user=request.user,

        movie_title=data['movie_title'],

        poster_path=data['poster_path']

    )

    serializer = FavoriteMovieSerializer(
        favorite
    )

    return Response(serializer.data)

# =========================
# GET USER FAVORITES
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_favorites(request):

    favorites = FavoriteMovie.objects.filter(
        user=request.user
    )

    serializer = FavoriteMovieSerializer(
        favorites,
        many=True
    )

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def remove_favorite(request, movie_id):

    favorite = get_object_or_404(

        FavoriteMovie,

        id=movie_id,

        user=request.user

    )

    favorite.delete()

    return Response({

        "message": "Removed from favorites"

    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_watch_history(request):

    data = request.data

    existing_movie = WatchedMovie.objects.filter(

        user=request.user,

        movie_title=data['movie_title']

    ).first()

    if existing_movie:

        return Response({
            "message": "Already in history"
        })

    watched_movie = WatchedMovie.objects.create(

        user=request.user,

        movie_title=data['movie_title'],

        poster_path=data['poster_path']

    )

    serializer = WatchedMovieSerializer(
        watched_movie
    )

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_watch_history(request):

    history = WatchedMovie.objects.filter(
        user=request.user
    ).order_by('-watched_at')

    serializer = WatchedMovieSerializer(
        history,
        many=True
    )

    return Response(serializer.data)