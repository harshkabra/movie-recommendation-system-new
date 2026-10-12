
from sklearn.metrics.pairwise import cosine_similarity
from src.data_loader import create_rating_matrix


def calculate_user_similarity(ratings_df=None):
    rating_matrix = create_rating_matrix(ratings_df)
    similarity_matrix = cosine_similarity(rating_matrix)
    return rating_matrix, similarity_matrix


def get_similar_users(user_id, n=5, ratings_df=None):
    rating_matrix, similarity_matrix = calculate_user_similarity(
        ratings_df
    )

    if user_id not in rating_matrix.index:
        return []

    user_index = rating_matrix.index.get_loc(user_id)
    user_similarities = similarity_matrix[user_index]

    similar_users = list(
        zip(rating_matrix.index, user_similarities)
    )

    similar_users.sort(
        key=lambda item: item[1],
        reverse=True
    )

    similar_users = [
        item for item in similar_users
        if item[0] != user_id
    ]

    return similar_users[:n]


def recommend_movies(user_id, n=10, ratings_df=None):
    rating_matrix = create_rating_matrix(ratings_df)

    if user_id not in rating_matrix.index:
        return []

    similar_users = get_similar_users(
        user_id,
        n=5,
        ratings_df=ratings_df
    )

    user_ratings = rating_matrix.loc[user_id]
    watched_movies = set(
        user_ratings[user_ratings > 0].index
    )

    movie_scores = {}

    for similar_user_id, similarity in similar_users:
        similar_user_ratings = rating_matrix.loc[
            similar_user_id
        ]

        for movie_id, rating in similar_user_ratings.items():
            if rating > 0 and movie_id not in watched_movies:
                if movie_id not in movie_scores:
                    movie_scores[movie_id] = []

                movie_scores[movie_id].append(
                    (rating, similarity)
                )

    recommendations = []


    recommendations = []

    if ratings_df is not None and not ratings_df.empty:
        global_mean = ratings_df["rating"].mean()
    else:
        from src.data_loader import prepare_ratings
        global_mean = prepare_ratings()["rating"].mean()

    prior_strength = 1.0

    for movie_id, ratings in movie_scores.items():
        total_weight = sum(
            similarity for rating, similarity in ratings
        )

        if total_weight > 0:
            weighted_rating_sum = sum(
                rating * similarity
                for rating, similarity in ratings
            )

            score = (
                weighted_rating_sum
                + prior_strength * global_mean
            ) / (
                total_weight + prior_strength
            )

            recommendations.append((movie_id, score))

    recommendations.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return recommendations[:n]