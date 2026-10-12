from src.data_loader import prepare_ratings, prepare_movies
from src.recommender import recommend_movies
from src.content_based import get_similar_movies
from src.hybrid_recommender import get_hybrid_recommendations

from sklearn.model_selection import train_test_split


# ----------------------------------------
# 1. Load data
# ----------------------------------------

ratings = prepare_ratings()
movies = prepare_movies()


# ----------------------------------------
# 2. Train/Test split
# ----------------------------------------

train_ratings, test_ratings = train_test_split(
    ratings,
    test_size=0.2,
    random_state=42
)


# ----------------------------------------
# 3. Select user and movie
# ----------------------------------------

user_id = 1

user_train = train_ratings[
    train_ratings["userId"] == user_id
]

movie_id = int(user_train.iloc[0]["movieId"])


# ----------------------------------------
# 4. Movie information
# ----------------------------------------

selected_movie = movies[
    movies["movieId"] == movie_id
]

movie_title = selected_movie.iloc[0]["title"]


print("=" * 60)
print("RECOMMENDATION QUALITY INSPECTION")
print("=" * 60)

print(f"\nUser ID: {user_id}")
print(f"Seed Movie: {movie_title}")
print(f"Movie ID: {movie_id}")


# ----------------------------------------
# 5. User-based recommendations
# ----------------------------------------

user_recommendations = recommend_movies(
    user_id=user_id,
    n=10,
    ratings_df=train_ratings
)

print("\n" + "=" * 60)
print("USER-BASED RECOMMENDATIONS")
print("=" * 60)

for index, (recommended_id, score) in enumerate(
    user_recommendations,
    start=1
):
    movie = movies[
        movies["movieId"] == recommended_id
    ]

    if not movie.empty:
        title = movie.iloc[0]["title"]

        print(
            f"{index}. {title} "
            f"| Score: {score:.4f}"
        )


# ----------------------------------------
# 6. Content-based recommendations
# ----------------------------------------

content_recommendations = get_similar_movies(
    movie_id=movie_id,
    n=10
)

print("\n" + "=" * 60)
print("CONTENT-BASED RECOMMENDATIONS")
print("=" * 60)

for index, (recommended_id, title, score) in enumerate(
    content_recommendations,
    start=1
):
    print(
        f"{index}. {title} "
        f"| Similarity: {score:.4f}"
    )


# ----------------------------------------
# 7. Hybrid recommendations
# ----------------------------------------

hybrid_recommendations = get_hybrid_recommendations(
    user_id=user_id,
    movie_id=movie_id,
    n=10,
    ratings_df=train_ratings
)

print("\n" + "=" * 60)
print("HYBRID RECOMMENDATIONS")
print("=" * 60)

for index, (recommended_id, score) in enumerate(
    hybrid_recommendations,
    start=1
):
    movie = movies[
        movies["movieId"] == recommended_id
    ]

    if not movie.empty:
        title = movie.iloc[0]["title"]

        print(
            f"{index}. {title} "
            f"| Hybrid Score: {score:.4f}"
        )


# ----------------------------------------
# 8. User's actual test ratings
# ----------------------------------------

user_test = test_ratings[
    (test_ratings["userId"] == user_id)
    & (test_ratings["rating"] >= 4)
].sort_values(
    "rating",
    ascending=False
)

print("\n" + "=" * 60)
print("USER'S ACTUAL TEST-SET LIKES")
print("=" * 60)

if user_test.empty:
    print("No test-set ratings >= 4 found.")

else:
    for index, row in user_test.head(10).iterrows():

        recommended_id = int(row["movieId"])
        rating = row["rating"]

        movie = movies[
            movies["movieId"] == recommended_id
        ]

        if not movie.empty:
            title = movie.iloc[0]["title"]

            print(
                f"{title} "
                f"| Actual Rating: {rating}"
            )