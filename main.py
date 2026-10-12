# from src.data_loader import load_movies, load_ratings, load_links


# movies = load_movies()
# ratings = load_ratings()
# links = load_links()


# print("========== DATASET SHAPE ==========")
# print("Movies:", movies.shape)
# print("Ratings:", ratings.shape)
# print("Links:", links.shape)


# print("\n========== DATASET COLUMNS ==========")

# print("Movies columns:")
# print(movies.columns.tolist())

# print("\nRatings columns:")
# print(ratings.columns.tolist())

# print("\nLinks columns:")
# print(links.columns.tolist())


# print("\n========== UNIQUE VALUES ==========")

# print("Unique users:", ratings["userId"].nunique())
# print("Unique movies in ratings:", ratings["movieId"].nunique())


# print("\n========== RATING INFORMATION ==========")

# print("Minimum rating:", ratings["rating"].min())
# print("Maximum rating:", ratings["rating"].max())
# print("Average rating:", ratings["rating"].mean())


# print("\n========== MISSING VALUES ==========")

# print("Movies missing values:")
# print(movies.isnull().sum())

# print("\nRatings missing values:")
# print(ratings.isnull().sum())

# print("\nLinks missing values:")
# print(links.isnull().sum())

# from src.data_loader import prepare_movies


# movies = prepare_movies()


# print("Prepared Movies:")
# print(movies.head())


# print("\nColumns:")
# print(movies.columns.tolist())


# print("\nShape:")
# print(movies.shape)

# from src.data_loader import prepare_ratings


# ratings = prepare_ratings()


# print("Prepared Ratings:")
# print(ratings.head())


# print("\nColumns:")
# print(ratings.columns.tolist())


# print("\nShape:")
# print(ratings.shape)


# from src.data_loader import create_rating_matrix


# rating_matrix = create_rating_matrix()


# print("Rating Matrix:")
# print(rating_matrix.iloc[:5, :10])


# print("\nMatrix Shape:")
# print(rating_matrix.shape)  


# from src.recommender import calculate_user_similarity


# similarity_matrix = calculate_user_similarity()


# print("Similarity Matrix:")
# print(similarity_matrix[:5, :5])


# print("\nSimilarity Matrix Shape:")
# print(similarity_matrix.shape)

# from src.recommender import get_similar_users


# similar_users = get_similar_users(1, 5)


# print("Similar Users for User 1:")

# for user_id, similarity in similar_users:
#     print(
#         f"User {user_id} - Similarity: {similarity:.4f}"
#     )



# from src.recommender import recommend_movies
# from src.data_loader import prepare_movies


# user_id = 1

# recommendations = recommend_movies(user_id, n=10)
# movies = prepare_movies()


# print(f"Recommended Movies for User {user_id}:\n")

# for movie_id, score in recommendations:
#     movie = movies[movies["movieId"] == movie_id]


#     if not movie.empty:
#         title = movie.iloc[0]["title"]
#         print(f"{title} - Predicted Score: {score:.2f}")



# from src.content_based import calculate_movie_similarity


# movies, similarity_matrix = calculate_movie_similarity()

# print("Movie Similarity Matrix:")
# print(similarity_matrix[:5, :5])

# print("\nMatrix Shape:")
# print(similarity_matrix.shape)


# from src.content_based import get_similar_movies


# movie_id = 1

# recommendations = get_similar_movies(movie_id, n=10)

# print("Movies similar to Toy Story (1995):\n")

# for movie_id, title, score in recommendations:
#     print(f"{title} - Similarity: {score:.4f}")


# from src.data_loader import prepare_movies

# movies = prepare_movies()

# movie_id = 1

# movie = movies[movies["movieId"] == movie_id]

# if not movie.empty:
#     title = movie.iloc[0]["title"]
#     genres = movie.iloc[0]["genres"]

#     print("Movie:", title)
#     print("Genres:", genres)
# else:
#     print("Movie not found.")



# from src.content_based import get_similar_movies
# from src.data_loader import prepare_movies


# movie_id = 1

# movies = prepare_movies()
# recommendations = get_similar_movies(movie_id, n=10)

# selected_movie = movies[movies["movieId"] == movie_id]

# if not selected_movie.empty:
#     print("Selected Movie:", selected_movie.iloc[0]["title"])
#     print("Genres:", selected_movie.iloc[0]["genres"])
#     print("\nSimilar Movies:\n")

#     for recommended_id, title, score in recommendations:
#         recommended_movie = movies[
#             movies["movieId"] == recommended_id
#         ]

#         if not recommended_movie.empty:
#             genres = recommended_movie.iloc[0]["genres"]

#             print(f"Movie: {title}")
#             print(f"Genres: {genres}")
#             print(f"Similarity: {score:.4f}")
#             print("-" * 50)
# else:
#     print("Movie not found.")



# from src.content_based import get_similar_movies
# from src.data_loader import prepare_movies

# movie_id = 1

# movies = prepare_movies()
# recommendations = get_similar_movies(movie_id, n=10)

# selected_movie = movies[movies["movieId"] == movie_id]

# if not selected_movie.empty:
#     print("Selected Movie:", selected_movie.iloc[0]["title"])
#     print("Genres:", selected_movie.iloc[0]["genres"])
#     print("\nSimilar Movies:\n")

#     for recommended_id, title, score in recommendations:
#         recommended_movie = movies[
#             movies["movieId"] == recommended_id
#         ]

#         if not recommended_movie.empty:
#             genres = recommended_movie.iloc[0]["genres"]

#             print(f"Movie: {title}")
#             print(f"Genres: {genres}")
#             print(f"Similarity: {score:.4f}")
#             print("-" * 40)
# else:
#     print("Movie not found.")



# from src.content_based import get_similar_movies
# from src.data_loader import prepare_movies

# movies = prepare_movies()

# search_title = input("Enter a movie title: ").strip().lower()

# matched_movies = movies[
#     movies["title"].str.lower().str.contains(
#         search_title, na=False, regex=False
#     )
# ]

# if matched_movies.empty:
#     print("No movie found. Please try another title.")

# else:
#     print("\nMatching Movies:\n")

#     for _, movie in matched_movies.head(10).iterrows():
#         print(f"Movie ID: {movie['movieId']} | {movie['title']}")

#     try:
#         movie_id = int(input("\nEnter the Movie ID: "))

#         selected_movie = movies[
#             movies["movieId"] == movie_id
#         ]

#         if selected_movie.empty:
#             print("Invalid Movie ID.")

#         else:
#             movie_title = selected_movie.iloc[0]["title"]
#             genres = selected_movie.iloc[0]["genres"]

#             print(f"\nSelected Movie: {movie_title}")
#             print(f"Genres: {genres}")
#             print("\nSimilar Movies:\n")

#             recommendations = get_similar_movies(
#                 movie_id, n=10
#             )

#             for rec_id, title, score in recommendations:
#                 print(f"{title} - Similarity: {score:.4f}")

#     except ValueError:
#         print("Please enter a valid numeric Movie ID.")


# from src.hybrid_recommender import get_hybrid_recommendations
# from src.data_loader import prepare_movies

# movies = prepare_movies()

# user_id = 1
# movie_id = 1

# selected_movie = movies[
#     movies["movieId"] == movie_id
# ]

# if not selected_movie.empty:

#     movie_title = selected_movie.iloc[0]["title"]

#     print(f"User ID: {user_id}")
#     print(f"Selected Movie: {movie_title}")
#     print("\nHybrid Recommendations:\n")

#     recommendations = get_hybrid_recommendations(
#         user_id,
#         movie_id,
#         n=10
#     )

#     for recommended_id, score in recommendations:

#         movie = movies[
#             movies["movieId"] == recommended_id
#         ]

#         if not movie.empty:

#             title = movie.iloc[0]["title"]

#             print(
#                 f"{title} - Hybrid Score: {score:.4f}"
#             )

# else:
#     print("Movie not found.")

# from src.hybrid_recommender import get_hybrid_recommendations
# from src.data_loader import prepare_movies

# movies = prepare_movies()

# user_id = 1
# movie_id = 1

# selected_movie = movies[
#     movies["movieId"] == movie_id
# ]

# if not selected_movie.empty:

#     movie_title = selected_movie.iloc[0]["title"]

#     print(f"User ID: {user_id}")
#     print(f"Selected Movie: {movie_title}")
#     print("\nHybrid Recommendations:\n")

#     recommendations = get_hybrid_recommendations(
#         user_id,
#         movie_id,
#         n=10
#     )

#     for recommended_id, score in recommendations:

#         movie = movies[
#             movies["movieId"] == recommended_id
#         ]

#         if not movie.empty:

#             title = movie.iloc[0]["title"]

#             print(
#                 f"{title} - Hybrid Score: {score:.4f}"
#             )

# else:
#     print("Movie not found.")


from src.data_loader import prepare_movies, prepare_ratings
from src.recommender import recommend_movies
from src.content_based import get_similar_movies
from src.hybrid_recommender import get_hybrid_recommendations


def main():
    movies = prepare_movies()

    print("=" * 50)
    print("MOVIE RECOMMENDATION SYSTEM")
    print("=" * 50)

    print("\nChoose Recommendation Method:")
    print("1. User-based")
    print("2. Content-based")
    print("3. Hybrid")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice not in {"1", "2", "3"}:
        print("Invalid choice. Please select 1, 2, or 3.")
        return

    movie_id = None
    user_id = None

    if choice in {"1", "3"}:
        try:
            user_id = int(input("Enter User ID: "))
        except ValueError:
            print("Invalid User ID. Please enter a number.")
            return

        if user_id not in set(prepare_ratings()["userId"]):
            print("User ID not found in ratings data.")
            return

    try:
        movie_id = int(input("Enter Movie ID: "))
    except ValueError:
        print("Invalid Movie ID. Please enter a number.")
        return

    selected_movie = movies[
        movies["movieId"] == movie_id
    ]

    if selected_movie.empty:
        print("Movie not found. Please enter a valid Movie ID.")
        return

    movie_title = selected_movie.iloc[0]["title"]

    print(f"\nSelected Movie: {movie_title}")

    if user_id is not None:
        print(f"User ID: {user_id}")

    if choice == "1":
        recommendations = recommend_movies(
            user_id=user_id,
            n=10
        )

        print("\nUSER-BASED RECOMMENDATIONS\n")

        for recommended_id, score in recommendations:
            movie = movies[
                movies["movieId"] == recommended_id
            ]

            if not movie.empty:
                title = movie.iloc[0]["title"]
                print(f"{title} - Predicted Rating: {score:.4f}")

    elif choice == "2":
        recommendations = get_similar_movies(
            movie_id=movie_id,
            n=10
        )

        print("\nCONTENT-BASED RECOMMENDATIONS\n")

        for recommended_id, title, score in recommendations:
            print(f"{title} - Genre Similarity: {score:.4f}")

    else:
        recommendations = get_hybrid_recommendations(
            user_id=user_id,
            movie_id=movie_id,
            n=10
        )

        print("\nHYBRID RECOMMENDATIONS\n")

        for recommended_id, score in recommendations:
            movie = movies[
                movies["movieId"] == recommended_id
            ]

            if not movie.empty:
                title = movie.iloc[0]["title"]
                print(f"{title} - Hybrid Score: {score:.4f}")


if __name__ == "__main__":
    main()