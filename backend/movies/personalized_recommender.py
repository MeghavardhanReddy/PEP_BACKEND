import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

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
# LOAD MODELS & INITIALIZE ON THE FLY
# =========================

svd_model = None

svd_model_path = os.path.join(
    MODEL_PATH,
    'svd_model.pkl'
)

if os.path.exists(svd_model_path):
    svd_model = joblib.load(
        svd_model_path
    )
    print("[OK] SVD model loaded")
else:
    print("[WARN] SVD model missing")

# Fit TF-IDF and indices on the fly to save RAM & disk space
try:
    movies['genres'] = movies['genres'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])
    
    indices = pd.Series(
        movies.index,
        index=movies['title']
    ).drop_duplicates()
    
    print("[OK] TF-IDF Matrix and Indices initialized on the fly")
except Exception as e:
    tfidf_matrix = None
    indices = None
    print(f"[ERROR] Failed to initialize on-the-fly models: {e}")

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

    if not svd_model or tfidf_matrix is None or indices is None:

        return ["AI recommendation engine unavailable"]

    try:

        idx = indices[movie_title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

    except:

        return ["Movie not found"]

    # Compute similarity row on the fly
    cosine_sim_row = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()

    sim_scores = list(
        enumerate(cosine_sim_row)
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