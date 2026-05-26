from django.urls import path

from .views import (
    register_user,
    add_favorite,
    get_favorites,
    remove_favorite,
    add_watch_history,
    get_watch_history
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    register_user,
    add_favorite,
    get_favorites
)

urlpatterns = [

    path(
        'register/',
        register_user
    ),

    path(
        'login/',
        TokenObtainPairView.as_view()
    ),

    path(
        'refresh/',
        TokenRefreshView.as_view()
    ),
    path(
        'favorites/add/',
        add_favorite
    ),
    path(
        'favorites/',
        get_favorites
),
    path(
    'favorites/add/',
    add_favorite
),

path(
    'favorites/',
    get_favorites
),

path(
    'favorites/remove/<int:movie_id>/',
    remove_favorite
),

path(
    'history/add/',
    add_watch_history
),

path(
    'history/',
    get_watch_history
),
]