from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data_loader import prepare_movies


def prepare_genre_matrix():
    movies = prepare_movies().copy()

    movies["genres"] = movies["genres"].fillna("")

    vectorizer = CountVectorizer(
        token_pattern=r"[^|]+",
        lowercase=True
    )

    genre_matrix = vectorizer.fit_transform(movies["genres"])

    return movies, genre_matrix


def get_similar_movies(movie_id, n=10):
    movies, genre_matrix = prepare_genre_matrix()

    matching_indices = movies.index[
        movies["movieId"] == movie_id
    ].tolist()

    if not matching_indices:
        return []

    movie_index = matching_indices[0]

    similarity_scores = cosine_similarity(
        genre_matrix[movie_index],
        genre_matrix
    ).flatten()

    ranked_indices = similarity_scores.argsort()[::-1]

    recommendations = []

    for index in ranked_indices:
        if index == movie_index:
            continue

        recommended_movie_id = int(
            movies.iloc[index]["movieId"]
        )

        title = movies.iloc[index]["title"]
        score = float(similarity_scores[index])

        recommendations.append(
            (recommended_movie_id, title, score)
        )

        if len(recommendations) >= n:
            break

    return recommendations
