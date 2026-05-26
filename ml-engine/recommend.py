import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv('../datasets/movies.csv')# Fill missing values
movies['genres'] = movies['genres'].fillna('')

# Convert genres into vectors
tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Calculate similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create index mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

def recommend(movie_title):

    movie_title = movie_title.lower()

    matching_movies = movies[movies['title'].str.lower().str.contains(movie_title)]

    if matching_movies.empty:
        print("Movie not found")
        return

    selected_movie = matching_movies.iloc[0]['title']

    print(f"\nSelected Movie: {selected_movie}")

    idx = indices[selected_movie]

    similarity_scores = list(enumerate(cosine_sim[idx]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[1:6]

    movie_indices = [i[0] for i in similarity_scores]

    recommendations = movies['title'].iloc[movie_indices]

    print("\nRecommended Movies:\n")

    for movie in recommendations:
        print(movie)

# Test
movie_name = input("Enter movie name: ")

recommend(movie_name)