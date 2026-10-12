
from sklearn.model_selection import train_test_split

from src.data_loader import prepare_ratings
from src.hybrid_recommender import get_hybrid_recommendations


def precision_at_k(user_id, movie_id, k=10):
    ratings = prepare_ratings()

    train_ratings, test_ratings = train_test_split(
        ratings,
        test_size=0.2,
        random_state=42
    )

    # User ki test ratings mein se liked movies
    user_test_ratings = test_ratings[
        (test_ratings["userId"] == user_id)
        & (test_ratings["rating"] >= 4)
    ]

    liked_movie_ids = set(user_test_ratings["movieId"])

    # Recommendations sirf training data se generate hongi
    recommendations = get_hybrid_recommendations(
        user_id,
        movie_id,
        n=k,
        ratings_df=train_ratings
    )

    recommended_movie_ids = [
        recommended_id
        for recommended_id, score in recommendations
    ]

    if not recommended_movie_ids:
        return 0.0

    relevant_count = sum(
        1
        for recommended_id in recommended_movie_ids
        if recommended_id in liked_movie_ids
    )

    return relevant_count / len(recommended_movie_ids)



def evaluate_multiple_users(number_of_users=20, k=10):
    ratings = prepare_ratings()

    train_ratings, test_ratings = train_test_split(
        ratings,
        test_size=0.2,
        random_state=42
    )

    # Test data mein maujood users select karo
    test_users = test_ratings["userId"].unique()

    # Training data mein bhi present users hi evaluate honge
    train_users = set(train_ratings["userId"].unique())

    eligible_users = [
        user_id
        for user_id in test_users
        if user_id in train_users
    ]

    eligible_users = eligible_users[:number_of_users]

    scores = []

    for user_id in eligible_users:
        user_test_ratings = test_ratings[
            (test_ratings["userId"] == user_id)
            & (test_ratings["rating"] >= 4)
        ]

        liked_movie_ids = set(
            user_test_ratings["movieId"]
        )

        if not liked_movie_ids:
            continue

        # User ki training ratings mein se ek movie select karo
        user_train_movies = train_ratings[
            train_ratings["userId"] == user_id
        ]["movieId"]

        if user_train_movies.empty:
            continue

        movie_id = int(user_train_movies.iloc[0])

        recommendations = get_hybrid_recommendations(
            user_id=user_id,
            movie_id=movie_id,
            n=k,
            ratings_df=train_ratings
        )

        recommended_movie_ids = [
            recommended_id
            for recommended_id, score in recommendations
        ]

        if not recommended_movie_ids:
            continue

        relevant_count = sum(
            1
            for recommended_id in recommended_movie_ids
            if recommended_id in liked_movie_ids
        )

        precision = relevant_count / len(recommended_movie_ids)
        scores.append(precision)

    if not scores:
        print("No users could be evaluated.")
        return 0.0

    average_precision = sum(scores) / len(scores)

    print(f"Users evaluated: {len(scores)}")
    print(f"Average Precision@{k}: {average_precision:.4f}")
    print(f"Average Precision@{k} (%): {average_precision * 100:.2f}%")

    return average_precision


def evaluate_precision_recall(
        number_of_users=20,
        k=10,
        user_weight=0.7,
        content_weight=0.3
):
    ratings = prepare_ratings()

    train_ratings, test_ratings = train_test_split(
        ratings,
        test_size=0.2,
        random_state=42
    )

    test_users = test_ratings["userId"].unique()
    train_users = set(train_ratings["userId"].unique())

    eligible_users = [
        user_id
        for user_id in test_users
        if user_id in train_users
    ][:number_of_users]

    precision_scores = []
    recall_scores = []

    for user_id in eligible_users:
        user_test_ratings = test_ratings[
            (test_ratings["userId"] == user_id)
            & (test_ratings["rating"] >= 4)
        ]

        liked_movie_ids = set(user_test_ratings["movieId"])

        if not liked_movie_ids:
            continue

        user_train_movies = train_ratings[
            train_ratings["userId"] == user_id
        ]["movieId"]

        if user_train_movies.empty:
            continue

        movie_id = int(user_train_movies.iloc[0])

        recommendations = get_hybrid_recommendations(
            user_id=user_id,
            movie_id=movie_id,
            n=k,
            ratings_df=train_ratings,
            user_weight=user_weight,
            content_weight=content_weight
        )

        recommended_movie_ids = [
            recommended_id
            for recommended_id, score in recommendations
        ]

        if not recommended_movie_ids:
            continue

        relevant_count = sum(
            1
            for recommended_id in recommended_movie_ids
            if recommended_id in liked_movie_ids
        )

        precision = relevant_count / len(recommended_movie_ids)
        recall = relevant_count / len(liked_movie_ids)

        precision_scores.append(precision)
        recall_scores.append(recall)

    if not precision_scores:
        print("No users could be evaluated.")
        return

    average_precision = sum(precision_scores) / len(precision_scores)
    average_recall = sum(recall_scores) / len(recall_scores)

    print(f"Users evaluated: {len(precision_scores)}")
    print(f"Precision@{k}: {average_precision:.4f}")
    print(f"Recall@{k}: {average_recall:.4f}")
    print(f"Precision@{k} (%): {average_precision * 100:.2f}%")
    print(f"Recall@{k} (%): {average_recall * 100:.2f}%")


def compare_recommenders(number_of_users=20, k=10):
    from src.recommender import recommend_movies
    from src.content_based import get_similar_movies

    ratings = prepare_ratings()

    train_ratings, test_ratings = train_test_split(
        ratings,
        test_size=0.2,
        random_state=42
    )

    test_users = test_ratings["userId"].unique()
    train_users = set(train_ratings["userId"].unique())

    eligible_users = [
        user_id
        for user_id in test_users
        if user_id in train_users
    ][:number_of_users]

    model_scores = {
        "User-based": [],
        "Content-based": [],
        "Hybrid": []
    }

    for user_id in eligible_users:
        user_test = test_ratings[
            (test_ratings["userId"] == user_id)
            & (test_ratings["rating"] >= 4)
        ]

        liked_movies = set(user_test["movieId"])

        if not liked_movies:
            continue

        user_train = train_ratings[
            train_ratings["userId"] == user_id
        ]

        if user_train.empty:
            continue

        # Seed movie training data se select hogi
        movie_id = int(user_train.iloc[0]["movieId"])

        watched_movies = set(user_train["movieId"])

        user_recs = recommend_movies(
            user_id=user_id,
            n=100,
            ratings_df=train_ratings
        )

        content_recs = get_similar_movies(
            movie_id=movie_id,
            n=100
        )

        hybrid_recs = get_hybrid_recommendations(
            user_id=user_id,
            movie_id=movie_id,
            n=100,
            ratings_df=train_ratings
        )

        # Teenon models ke outputs ko movie IDs mein convert karo
        user_ids = [movie_id for movie_id, score in user_recs]

        content_ids = [
            movie_id for movie_id, title, score in content_recs
        ]

        hybrid_ids = [
            movie_id for movie_id, score in hybrid_recs
        ]

        recommendations_by_model = {
            "User-based": user_ids,
            "Content-based": content_ids,
            "Hybrid": hybrid_ids
        }

        for model_name, movie_ids in recommendations_by_model.items():
            # Training mein already watched movies hatao
            unseen_ids = [
                recommended_id
                for recommended_id in movie_ids
                if recommended_id not in watched_movies
                and recommended_id != movie_id
            ]

            top_ids = unseen_ids[:k]

            if not top_ids:
                continue

            relevant_count = sum(
                1 for recommended_id in top_ids
                if recommended_id in liked_movies
            )

            precision = relevant_count / len(top_ids)
            recall = relevant_count / len(liked_movies)

            model_scores[model_name].append(
                (precision, recall)
            )

    print(f"Evaluation results for up to {number_of_users} users")
    print("-" * 55)

    for model_name, scores in model_scores.items():
        if not scores:
            print(f"{model_name}: No users evaluated")
            continue

        avg_precision = sum(
            precision for precision, recall in scores
        ) / len(scores)

        avg_recall = sum(
            recall for precision, recall in scores
        ) / len(scores)

        print(f"\n{model_name}")
        print(f"Users evaluated: {len(scores)}")
        print(f"Precision@{k}: {avg_precision:.4f}")
        print(f"Recall@{k}: {avg_recall:.4f}")
