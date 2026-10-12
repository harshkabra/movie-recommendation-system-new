
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

from src.data_loader import prepare_movies, prepare_ratings
from src.recommender import recommend_movies
from src.content_based import get_similar_movies
from src.hybrid_recommender import get_hybrid_recommendations


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CineMatch | Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).parent
POSTER_DIR = BASE_DIR / "assets" / "posters"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #10131c;
        color: #f5f5f5;
    }

    [data-testid="stSidebar"] {
        background-color: #191e2b;
    }

    .main-title {
        font-size: 44px;
        font-weight: 800;
        color: #f5f5f5;
        margin-bottom: 0;
    }

    .subtitle {
        color: #a9b0c3;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .movie-card {
        background-color: #1b2130;
        border: 1px solid #30394c;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }

    .movie-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #ffffff;
    }

    .movie-info {
        font-size: 13px;
        color: #b9c1d3;
        margin-bottom: 6px;
    }

    .score {
        color: #f6c453;
        font-size: 15px;
        font-weight: 700;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    movies = prepare_movies()
    ratings = prepare_ratings()

    return movies, ratings


try:
    movies, ratings = load_data()
except Exception as error:
    st.error("Could not load the movie dataset.")
    st.exception(error)
    st.stop()


# =========================================================
# LOCAL POSTER FUNCTION
# =========================================================

def display_movie_poster(movie_id):
    """
    Display a local movie poster based on movieId.

    Supported filenames:
    assets/posters/1.jpg
    assets/posters/2.jpg
    assets/posters/3.jpg
    """

    movie_id = int(movie_id)

    possible_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    ]

    poster_path = None

    for extension in possible_extensions:
        candidate = POSTER_DIR / f"{movie_id}{extension}"

        if candidate.is_file():
            poster_path = candidate
            break

    if poster_path is not None:
        try:
            with Image.open(poster_path) as image:
                st.image(
                    image.copy(),
                    use_container_width=True,
                )
        except Exception:
            st.markdown(
                """
                <div style="
                    height: 220px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: #202431;
                    border-radius: 10px;
                    font-size: 42px;
                ">🎬</div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div style="
                height: 220px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #202431;
                border: 1px solid #30394c;
                border-radius: 10px;
                font-size: 42px;
            ">🎬</div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def find_movie_title(movie_id):
    matched = movies[movies["movieId"] == int(movie_id)]

    if matched.empty:
        return f"Movie ID {movie_id}"

    return matched.iloc[0]["title"]


def find_movie_genres(movie_id):
    matched = movies[movies["movieId"] == int(movie_id)]

    if matched.empty:
        return "Genres unavailable"

    genres = matched.iloc[0].get("genres", "")

    if pd.isna(genres) or not genres:
        return "Genres unavailable"

    return str(genres).replace("|", " • ")


def get_recommendation_score(score):
    try:
        return float(score)
    except (TypeError, ValueError):
        return 0.0


def display_recommendation_cards(results, method_name):
    if results is None or len(results) == 0:
        st.warning(
            "No recommendations were found. "
            "Try another movie or recommendation method."
        )
        return

    st.markdown(
        f'<div class="section-title">{method_name} Results</div>',
        unsafe_allow_html=True,
    )

    for start in range(0, len(results), 4):
        batch = results[start:start + 4]
        columns = st.columns(4)

        for column, result in zip(columns, batch):
            # Content-based results:
            # (movie_id, title, score)
            #
            # User-based and hybrid results:
            # (movie_id, score)

            movie_id = int(result[0])

            if method_name == "Content-Based":
                movie_title = str(result[1])
                score = get_recommendation_score(result[2])
            else:
                movie_title = find_movie_title(movie_id)
                score = get_recommendation_score(result[1])

            genres = find_movie_genres(movie_id)

            with column:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                display_movie_poster(movie_id)

                st.markdown(
                    f'<div class="movie-title">{movie_title}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="movie-info">{genres}</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f'<div class="score">⭐ Score: {score:.3f}</div>',
                    unsafe_allow_html=True,
                )

                st.caption(f"Movie ID: {movie_id}")

                st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🎬 CineMatch")
st.sidebar.caption("Movie Recommendation System")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Recommendations", "About"],
)

st.sidebar.divider()

st.sidebar.info(
    "Discover movies using user preferences, "
    "movie genres, and a hybrid recommendation approach."
)


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    st.markdown(
        '<div class="main-title">🎬 CineMatch</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Discover your next favourite movie."
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Movies", f"{movies['movieId'].nunique():,}")
    col2.metric("Total Ratings", f"{len(ratings):,}")
    col3.metric("Unique Users", f"{ratings['userId'].nunique():,}")

    st.divider()

    st.markdown(
        '<div class="section-title">Explore CineMatch</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "CineMatch recommends movies using three approaches. "
        "Open Recommendations in the sidebar to get started."
    )

    feature1, feature2, feature3 = st.columns(3)

    with feature1:
        st.subheader("👥 User-Based")
        st.write(
            "Find movies rated highly by users "
            "with similar rating patterns."
        )

    with feature2:
        st.subheader("🎭 Content-Based")
        st.write(
            "Discover movies with genres similar "
            "to a movie you already like."
        )

    with feature3:
        st.subheader("🔀 Hybrid")
        st.write(
            "Combine user preferences and movie "
            "similarity for recommendations."
        )

    st.divider()

    with st.expander("Preview movie dataset"):
        st.dataframe(
            movies.head(20),
            use_container_width=True,
        )


# =========================================================
# RECOMMENDATIONS PAGE
# =========================================================

elif page == "Recommendations":

    st.markdown(
        '<div class="main-title">Movie Recommendations</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "Choose a method and discover movies."
        "</div>",
        unsafe_allow_html=True,
    )

    method = st.selectbox(
        "Recommendation Method",
        [
            "Content-Based",
            "User-Based",
            "Hybrid",
        ],
    )

    st.divider()

    selected_movie_id = None
    selected_movie_title = None

    # -----------------------------------------------------
    # MOVIE SEARCH
    # -----------------------------------------------------

    search_query = st.text_input(
        "Search for a movie",
        placeholder="Example: Toy Story",
    )

    if search_query.strip():
        matched_movies = movies[
            movies["title"].str.contains(
                search_query.strip(),
                case=False,
                na=False,
                regex=False,
            )
        ].sort_values("title")

        st.caption(
            f"Found {len(matched_movies)} matching movie(s)."
        )

        if matched_movies.empty:
            st.warning(
                "No matching movies found. "
                "Try another title or spelling."
            )
        else:
            movie_options = {
                f"{row['title']} (ID: {int(row['movieId'])})":
                    int(row["movieId"])
                for _, row in matched_movies.head(100).iterrows()
            }

            selected_option = st.selectbox(
                "Select a movie",
                list(movie_options.keys()),
            )

            selected_movie_id = movie_options[selected_option]
            selected_movie_title = find_movie_title(selected_movie_id)

            info_col1, info_col2 = st.columns([1, 2])

            with info_col1:
                display_movie_poster(selected_movie_id)

            with info_col2:
                st.subheader(selected_movie_title)

                st.write(
                    f"**Movie ID:** {selected_movie_id}"
                )

                st.write(
                    f"**Genres:** {find_movie_genres(selected_movie_id)}"
                )

    # -----------------------------------------------------
    # USER SELECTION
    # -----------------------------------------------------

    user_id = None

    if method in ["User-Based", "Hybrid"]:
        available_users = sorted(
            ratings["userId"].dropna().unique().tolist()
        )

        if available_users:
            user_id = st.selectbox(
                "Select User ID",
                available_users,
                index=0,
            )
        else:
            st.error("No users are available in the ratings dataset.")

    number_of_recommendations = st.slider(
        "Number of recommendations",
        min_value=5,
        max_value=20,
        value=10,
        step=5,
    )

    # -----------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # -----------------------------------------------------

    generate = st.button(
        "✨ Generate Recommendations",
        type="primary",
        use_container_width=True,
    )

    if generate:

        if method in ["Content-Based", "Hybrid"] and selected_movie_id is None:
            st.warning(
                "Please search for and select a movie first."
            )

        elif method in ["User-Based", "Hybrid"] and user_id is None:
            st.warning(
                "No valid user is available in the dataset."
            )

        else:
            try:
                with st.spinner("Finding the best movies for you..."):

                    if method == "Content-Based":
                        results = get_similar_movies(
                            selected_movie_id,
                            n=number_of_recommendations,
                        )

                    elif method == "User-Based":
                        results = recommend_movies(
                            int(user_id),
                            n=number_of_recommendations,
                        )

                    else:
                        results = get_hybrid_recommendations(
                            int(user_id),
                            selected_movie_id,
                            n=number_of_recommendations,
                        )

                display_recommendation_cards(
                    results,
                    method,
                )

            except Exception as error:
                st.error(
                    "Something went wrong while generating "
                    "recommendations."
                )

                st.exception(error)


# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "About":

    st.markdown(
        '<div class="main-title">About CineMatch</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="subtitle">'
        "A movie recommendation project built with Python."
        "</div>",
        unsafe_allow_html=True,
    )

    st.subheader("Technology Stack")

    st.markdown(
        """
        - **Python** — application logic
        - **Pandas** — loading and processing CSV datasets
        - **Scikit-learn** — similarity calculations used by the recommendation models
        - **Streamlit** — interactive user interface
        - **Pillow** — opening and displaying local poster images
        - **CSV files** — movie, rating, and external-ID metadata
        """
    )

    st.subheader("Recommendation Methods")

    st.markdown(
        """
        **1. User-Based Collaborative Filtering**

        Uses similarities between users' rating patterns.

        **2. Content-Based Filtering**

        Recommends movies based on genre similarity.

        **3. Hybrid Recommendation**

        Combines signals from the existing user-based and content-based approaches.
        """
    )

    st.subheader("Local Movie Posters")

    st.write(
        "Poster images are loaded from the assets/posters folder. "
        "Name each file using its movieId, for example 1.jpg. "
        "When no local image exists, CineMatch displays a placeholder."
    )

    st.caption(
        "CineMatch uses the existing CSV dataset and recommendation code. "
        "No external movie API or database is required."
    )
