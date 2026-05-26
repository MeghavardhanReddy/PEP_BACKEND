import os
import pandas as pd
import joblib

from accounts.models import (
    FavoriteMovie,
    WatchedMovie
)

# =========================
# BASE PATHS
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    'datasets'
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    'ml-engine',
    'saved_models'
)

# =========================
# LOAD DATASETS
# =========================

movies = pd.read_csv(
    os.path.join(
        DATASET_PATH,
        'movies.csv'
    )
)

# =========================
# LOAD MODELS SAFELY
# =========================

svd_model = None
cosine_sim = None
indices = None

svd_model_path = os.path.join(
    MODEL_PATH,
    'svd_model.pkl'
)

cosine_path = os.path.join(
    MODEL_PATH,
    'cosine_sim.pkl'
)

indices_path = os.path.join(
    MODEL_PATH,
    'indices.pkl'
)

if os.path.exists(svd_model_path):

    svd_model = joblib.load(
        svd_model_path
    )

    print("[OK] SVD model loaded")

else:

    print("[WARN] SVD model missing")

if os.path.exists(cosine_path):

    cosine_sim = joblib.load(
        cosine_path
    )

    print("[OK] Cosine similarity loaded")

else:

    print("[WARN] Cosine similarity missing")

if os.path.exists(indices_path):

    indices = joblib.load(
        indices_path
    )

    print("[OK] Indices loaded")

else:

    print("[WARN] Indices missing")

# =========================
# USER PREFERENCE LEARNING
# =========================

def get_user_preferences(user):

    favorite_movies = FavoriteMovie.objects.filter(
        user=user
    )

    watched_movies = WatchedMovie.objects.filter(
        user=user
    )

    user_preferences = []

    for movie in favorite_movies:

        user_preferences.append({
            "title": movie.movie_title,
            "weight": 3
        })

    for movie in watched_movies:

        user_preferences.append({
            "title": movie.movie_title,
            "weight": 1.5
        })

    return user_preferences

# =========================
# PERSONALIZED AI
# =========================

def personalized_recommendation(

    movie_title,
    user,
    top_n=10

):

    if not svd_model or cosine_sim is None or indices is None:

        return ["AI recommendation engine unavailable"]

    try:

        idx = indices[movie_title]

    except:

        return ["Movie not found"]

    sim_scores = list(
        enumerate(cosine_sim[idx])
    )

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    sim_scores = sim_scores[1:40]

    movie_indices = [
        i[0] for i in sim_scores
    ]

    candidate_movies = movies.iloc[
        movie_indices
    ][['movieId', 'title', 'genres']]

    user_preferences = get_user_preferences(
        user
    )

    predictions = []

    for _, row in candidate_movies.iterrows():

        predicted_rating = svd_model.predict(
            user.id,
            row['movieId']
        ).est

        preference_bonus = 0

        for pref_movie in user_preferences:

            if pref_movie["title"].lower() in row['title'].lower():

                preference_bonus += pref_movie["weight"]

        final_score = (
            predicted_rating +
            preference_bonus
        )

        predictions.append(

            (
                row['title'],
                final_score
            )

        )

    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = [

        movie[0]
        for movie in predictions[:top_n]

    ]

    return recommendations