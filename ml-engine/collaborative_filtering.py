import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse

# Load datasets
ratings = pd.read_csv('../datasets/ratings.csv')
movies = pd.read_csv('../datasets/movies.csv')

print("Datasets Loaded Successfully!")

# Reader object
reader = Reader(rating_scale=(0.5, 5.0))

# Load into Surprise
data = Dataset.load_from_df(
    ratings[['userId', 'movieId', 'rating']],
    reader
)

# Train-test split
trainset, testset = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

# SVD Model
model = SVD()

print("Training Model...")

# Train model
model.fit(trainset)

print("Training Completed!")

# Test model
predictions = model.test(testset)

# Accuracy
rmse(predictions)

# -----------------------------
# Recommend movies for a user
# -----------------------------

user_id = 1

# Movies already watched
watched_movies = ratings[ratings['userId'] == user_id]['movieId'].tolist()

# Movies not watched
all_movies = movies['movieId'].tolist()

unwatched_movies = [
    movie for movie in all_movies
    if movie not in watched_movies
]

# Predict ratings
predictions = []

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

# Top 10 recommendations
top_recommendations = predictions[:10]

print("\nTop Recommendations:\n")

for movie_id, predicted_rating in top_recommendations:

    movie_title = movies[
        movies['movieId'] == movie_id
    ]['title'].values[0]

    print(
        f"{movie_title} "
        f"(Predicted Rating: {predicted_rating:.2f})"
    )