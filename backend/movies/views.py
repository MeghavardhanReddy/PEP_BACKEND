from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .personalized_recommender import (
    personalized_recommendation
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def recommend_movies(request):

    user_id = request.GET.get('user_id', 1)

    movie = request.GET.get('movie')

    recommendations = personalized_recommendation(
        movie,
        request.user
)

    return Response({
        "recommendations": recommendations
    })