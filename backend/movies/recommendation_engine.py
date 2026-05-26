import pandas as pd
from surprise import Dataset, Reader, SVD

import os

# BASE DIR & PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets')

# Load datasets
ratings = pd.read_csv(os.path.join(DATASET_PATH, 'ratings.csv'))
movies = pd.read_csv(os.path.join(DATASET_PATH, 'movies.csv'))

# Reader object
reader = Reader(rating_scale=(0.5, 5.0))

# Load dataset
data = Dataset.load_from_df(
    ratings[['userId', 'movieId', 'rating']],
    reader
)

# Build full trainset
trainset = data.build_full_trainset()

# Train model
model = SVD()
model.fit(trainset)

print("AI Recommendation Model Ready!")

# -----------------------------
# Recommendation Function
# -----------------------------

def get_user_recommendations(user_id=1, top_n=10):

    # Movies watched by user
    watched_movies = ratings[
        ratings['userId'] == user_id
    ]['movieId'].tolist()

    # All movies
    all_movies = movies['movieId'].tolist()

    # Unwatched movies
    unwatched_movies = [
        movie for movie in all_movies
        if movie not in watched_movies
    ]

    predictions = []

    # Predict ratings
    for movie_id in unwatched_movies:

        predicted_rating = model.predict(
            user_id,
            movie_id
        ).est

        predictions.append(
            (movie_id, predicted_rating)
        )

    # Sort by predicted rating
    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Top recommendations
    top_recommendations = predictions[:top_n]

    recommended_movies = []

    for movie_id, rating in top_recommendations:

        movie_title = movies[
            movies['movieId'] == movie_id
        ]['title'].values[0]

        recommended_movies.append(movie_title)

    return recommended_movies