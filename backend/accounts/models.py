from django.db import models
from django.contrib.auth.models import User


class FavoriteMovie(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    movie_title = models.CharField(
        max_length=255
    )

    poster_path = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.movie_title}"

class WatchedMovie(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    movie_title = models.CharField(
        max_length=255
    )

    poster_path = models.TextField()

    watched_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} watched {self.movie_title}"