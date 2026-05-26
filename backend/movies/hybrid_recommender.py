import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from surprise import Dataset, Reader, SVD

import os

# BASE DIR & PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets')

# -----------------------------
# LOAD DATASETS
# -----------------------------

movies = pd.read_csv(os.path.join(DATASET_PATH, 'movies.csv'))
ratings = pd.read_csv(os.path.join(DATASET_PATH, 'ratings.csv'))

# -----------------------------
# CONTENT-BASED FILTERING
# -----------------------------

movies['genres'] = movies['genres'].fillna('')

tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(movies['genres'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(
    movies.index,
    index=movies['title']
).drop_duplicates()

# -----------------------------
# COLLABORATIVE FILTERING
# -----------------------------

reader = Reader(rating_scale=(0.5, 5.0))

data = Dataset.load_from_df(
    ratings[['userId', 'movieId', 'rating']],
    reader
)

trainset = data.build_full_trainset()

svd_model = SVD()

svd_model.fit(trainset)

print("Hybrid AI Model Ready!")

# -----------------------------
# HYBRID RECOMMENDATION
# -----------------------------

def hybrid_recommendation(movie_title, user_id=1):

    try:

        idx = indices[movie_title]

    except:

        return ["Movie not found"]

    # Content-based similarity
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

    # Collaborative filtering score
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

    # Sort by predicted rating
    predictions.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Top 10
    recommendations = [
        movie[0]
        for movie in predictions[:10]
    ]

    return recommendations