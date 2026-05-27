import os
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# =========================
# BASE PATHS
# =========================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), 'datasets')
MODEL_PATH = os.path.join(SCRIPT_DIR, 'saved_models')

# Create saved_models directory if it doesn't exist
os.makedirs(MODEL_PATH, exist_ok=True)

# =========================
# LOAD DATASETS
# =========================

movies = pd.read_csv(
    os.path.join(DATASET_PATH, 'movies.csv')
)

ratings = pd.read_csv(
    os.path.join(DATASET_PATH, 'ratings.csv')
)

print("Datasets Loaded")

# =========================
# PREPROCESSING
# =========================

movies['genres'] = movies['genres'].fillna('')

print("Preprocessing Complete")

# =========================
# TF-IDF FEATURE EXTRACTION
# =========================

tfidf = TfidfVectorizer(
    stop_words='english'
)

tfidf_matrix = tfidf.fit_transform(
    movies['genres']
)

cosine_sim = cosine_similarity(
    tfidf_matrix,
    tfidf_matrix
)

indices = pd.Series(
    movies.index,
    index=movies['title']
).drop_duplicates()

print("Content-Based Features Ready")

# =========================
# COLLABORATIVE FILTERING
# =========================

reader = Reader(
    rating_scale=(0.5, 5.0)
)

data = Dataset.load_from_df(
    ratings[['userId', 'movieId', 'rating']],
    reader
)

# Train/Test Split
trainset, testset = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

# Train SVD Model
svd_model = SVD(
    n_factors=100,
    n_epochs=30,
    lr_all=0.005,
    reg_all=0.02
)

svd_model.fit(trainset)

print("SVD Model Trained")

# =========================
# MODEL EVALUATION
# =========================

predictions = svd_model.test(testset)

rmse = accuracy.rmse(
    predictions
)

mae = accuracy.mae(
    predictions
)

print(f"RMSE: {rmse}")
print(f"MAE: {mae}")

# =========================
# SAVE MODELS
# =========================

joblib.dump(
    svd_model,
    os.path.join(MODEL_PATH, 'svd_model.pkl')
)

joblib.dump(
    tfidf,
    os.path.join(MODEL_PATH, 'tfidf.pkl')
)

# Skip saving the extremely large cosine similarity matrix (759MB)
# to stay under the Render free tier 512MB RAM and build limits.
# cosine_sim is calculated on the fly at recommendation time.
# joblib.dump(
#     cosine_sim,
#     os.path.join(MODEL_PATH, 'cosine_sim.pkl')
# )

joblib.dump(
    indices,
    os.path.join(MODEL_PATH, 'indices.pkl')
)

print("Models Saved Successfully")