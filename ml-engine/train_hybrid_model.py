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
# LOAD DATASETS
# =========================

movies = pd.read_csv(
    '../datasets/movies.csv'
)

ratings = pd.read_csv(
    '../datasets/ratings.csv'
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
    'saved_models/svd_model.pkl'
)

joblib.dump(
    tfidf,
    'saved_models/tfidf.pkl'
)

joblib.dump(
    cosine_sim,
    'saved_models/cosine_sim.pkl'
)

joblib.dump(
    indices,
    'saved_models/indices.pkl'
)

print("Models Saved Successfully")