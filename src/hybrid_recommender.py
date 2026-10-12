
from src.recommender import recommend_movies
from src.content_based import get_similar_movies


def get_hybrid_recommendations(
    user_id,
    movie_id,
    n=10,
    ratings_df=None,
    user_weight=0.7,
    content_weight=0.3
):
    user_recommendations = recommend_movies(
        user_id,
        n=100,
        ratings_df=ratings_df
    )

    content_recommendations = get_similar_movies(
        movie_id,
        n=100
    )

    user_scores = {}
    content_scores = {}

    if user_recommendations:
        max_rating = max(
            score for _, score in user_recommendations
        )

        for recommended_id, score in user_recommendations:
            if max_rating > 0:
                user_scores[recommended_id] = score / max_rating
            else:
                user_scores[recommended_id] = 0

    if content_recommendations:
        max_similarity = max(
            score for _, _, score in content_recommendations
        )

        for recommended_id, title, score in content_recommendations:
            if max_similarity > 0:
                content_scores[recommended_id] = (
                    score / max_similarity
                )
            else:
                content_scores[recommended_id] = 0

    all_movie_ids = set(user_scores) | set(content_scores)

    hybrid_scores = {}

    for recommended_id in all_movie_ids:
        user_score = user_scores.get(recommended_id, 0)
        content_score = content_scores.get(recommended_id, 0)

        hybrid_score = (
            user_weight * user_score
            + content_weight * content_score
        )

        hybrid_scores[recommended_id] = hybrid_score

    hybrid_scores.pop(movie_id, None)

    ranked_movies = sorted(
        hybrid_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ranked_movies[:n]
