import os
import pandas as pd
import joblib

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

ratings = pd.read_csv(
    os.path.join(
        DATASET_PATH,
        'ratings.csv'
    )
)

# =========================
# LOAD MODELS
# =========================

svd_model = joblib.load(
    os.path.join(
        MODEL_PATH,
        'svd_model.pkl'
    )
)

tfidf = joblib.load(
    os.path.join(
        MODEL_PATH,
        'tfidf.pkl'
    )
)

cosine_sim = joblib.load(
    os.path.join(
        MODEL_PATH,
        'cosine_sim.pkl'
    )
)

indices = joblib.load(
    os.path.join(
        MODEL_PATH,
        'indices.pkl'
    )
)

print("AI Models Loaded Successfully!")

# =========================
# HYBRID RECOMMENDER
# =========================

def hybrid_recommendation(
    movie_title,
    user_id=1,
    top_n=10
):

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

    sim_scores = sim_scores[1:30]

    movie_indices = [
        i[0] for i in sim_scores
    ]

    candidate_movies = movies.iloc[
        movie_indices
    ][['movieId', 'title']]

    predictions = []

    for _, row in candidate_movies.iterrows():

        predicted_rating = svd_model.predict(
            user_id,
            row['movieId']
        ).est

        predictions.append(
            (
                row['title'],
                predicted_rating
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