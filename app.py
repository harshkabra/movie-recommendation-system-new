
from pathlib import Path

import pandas as pd
import streamlit as st

from src.data_loader import prepare_movies, prepare_ratings
from src.recommender import recommend_movies
from src.content_based import get_similar_movies
from src.hybrid_recommender import get_hybrid_recommendations


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CineMatch | Movie Discovery",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CINEMATIC DARK THEME
# =========================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --background: #0b0b0f;
        --surface: #15151d;
        --surface-light: #20202a;
        --accent: #e50914;
        --accent-hover: #ff2833;
        --text: #f5f5f7;
        --muted: #a1a1ad;
        --border: #30303b;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 11, 15, 0.92);
    }

    [data-testid="stSidebar"] {
        background: #111117;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .brand {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .brand span {
        color: var(--accent);
    }

    .muted {
        color: var(--muted);
    }

    .eyebrow {
        color: #ff5962;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }

    .hero {
        background:
            radial-gradient(
                circle at 85% 15%,
                rgba(229, 9, 20, 0.20),
                transparent 36%
            ),
            linear-gradient(135deg, #20202a, #111117 70%);
        border: 1px solid #35313a;
        border-radius: 20px;
        padding: 2.5rem 2.2rem;
        margin: 0.5rem 0 1.7rem 0;
    }

    .hero h1 {
        font-size: clamp(2.2rem, 5vw, 3.7rem);
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -2px;
        margin: 0 0 1rem 0;
    }

    .hero h1 span {
        color: var(--accent);
    }

    .hero p {
        color: #c1c1cb;
        font-size: 1.05rem;
        line-height: 1.8;
        max-width: 650px;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 750;
        margin: 1.3rem 0 0.3rem 0;
    }

    .section-subtitle {
        color: var(--muted);
        margin-bottom: 1.2rem;
    }

    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.2rem;
        min-height: 115px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: var(--text);
        font-size: 1.8rem;
        font-weight: 800;
    }

    .movie-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.1rem;
        min-height: 170px;
        height: 100%;
        margin-bottom: 0.6rem;
        transition: border-color 0.2s ease;
    }

    .movie-card:hover {
        border-color: var(--accent);
    }

    .movie-rank {
        color: #ff5962;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 0.6rem;
    }

    .movie-title {
        color: var(--text);
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.45;
        margin-bottom: 0.65rem;
        overflow-wrap: anywhere;
    }

    .movie-genres {
        color: var(--muted);
        font-size: 0.82rem;
        line-height: 1.6;
        margin-bottom: 0.9rem;
    }

    .score {
        display: inline-block;
        color: #ff7b83;
        background: rgba(229, 9, 20, 0.12);
        border: 1px solid rgba(229, 9, 20, 0.25);
        border-radius: 20px;
        padding: 0.35rem 0.65rem;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .feature-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.3rem;
        min-height: 155px;
    }

    .feature-icon {
        font-size: 1.7rem;
        margin-bottom: 0.6rem;
    }

    .feature-title {
        font-weight: 750;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.7;
    }

    .stButton > button {
        background: var(--accent);
        color: white;
        border: 1px solid var(--accent);
        border-radius: 9px;
        font-weight: 700;
        padding: 0.65rem 1rem;
        transition: background 0.2s ease;
    }

    .stButton > button:hover {
        background: var(--accent-hover);
        border-color: var(--accent-hover);
        color: white;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #17171f;
        border-color: var(--border);
        border-radius: 9px;
    }

    div[data-testid="stSlider"] {
        padding-top: 0.4rem;
    }

    hr {
        border-color: var(--border);
        margin: 1.6rem 0;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    @media (max-width: 768px) {
        .hero {
            padding: 1.5rem;
        }

        .hero h1 {
            letter-spacing: -1px;
        }
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
    st.error("CineMatch could not load the CSV dataset.")
    st.code(str(error))
    st.info(
        "Check that movies.csv, ratings.csv, and links.csv "
        "are available in your configured data directory."
    )
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_movie_title(movie_id):
    matched = movies[movies["movieId"] == movie_id]

    if matched.empty:
        return f"Movie ID {movie_id}"

    return str(matched.iloc[0]["title"])


def get_movie_genres(movie_id):
    matched = movies[movies["movieId"] == movie_id]

    if matched.empty:
        return "Genres unavailable"

    genres = matched.iloc[0].get("genres", "Genres unavailable")

    if pd.isna(genres) or genres == "":
        return "Genres unavailable"

    return str(genres).replace("|", " · ")


def display_metric(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_movie_card(movie_id, score, rank, method_name):
    title = get_movie_title(movie_id)
    genres = get_movie_genres(movie_id)

    st.markdown(
        f"""
        <div class="movie-card">
            <div class="movie-rank">
                #{rank:02d} &nbsp; RECOMMENDED
            </div>
            <div class="movie-title">{title}</div>
            <div class="movie-genres">{genres}</div>
            <span class="score">
                {method_name}: {float(score):.4f}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_recommendation_cards(results, method_name):
    if not results:
        st.warning(
            "No recommendations were returned. "
            "Try another user or movie."
        )
        return

    st.markdown(
        f"""
        <div class="section-title">Your recommendations</div>
        <div class="section-subtitle">
            Results from {method_name} filtering
        </div>
        """,
        unsafe_allow_html=True,
    )

    columns_per_row = 3

    for start in range(0, len(results), columns_per_row):
        columns = st.columns(columns_per_row, gap="medium")

        for offset, result in enumerate(
            results[start:start + columns_per_row]
        ):
            if method_name == "Content-Based":
                movie_id, title, score = result
            else:
                movie_id, score = result

            with columns[offset]:
                display_movie_card(
                    movie_id=movie_id,
                    score=score,
                    rank=start + offset + 1,
                    method_name=method_name,
                )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">Cine<span>Match</span> 🎬</div>',
        unsafe_allow_html=True,
    )

    st.caption("YOUR PERSONAL MOVIE DISCOVERY SPACE")

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        ["Home", "Recommendations", "About"],
        index=0,
    )

    st.markdown("---")

    st.markdown("**DISCOVER SOMETHING NEW**")
    st.caption(
        "Find movies through your preferences, "
        "movie genres, or a combination of both."
    )

    st.markdown("---")
    st.caption("CineMatch · MovieLens Dataset")


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">YOUR NEXT FAVORITE MOVIE</div>
            <h1>Every movie night<br>starts with <span>CineMatch.</span></h1>
            <p>
                Discover movies tailored to your interests.
                Explore similar titles, find recommendations
                based on user ratings, and try our hybrid approach.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    movie_count = movies["movieId"].nunique()
    user_count = ratings["userId"].nunique()
    rating_count = len(ratings)

    st.markdown(
        '<div class="section-title">Inside your movie universe</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        'A quick look at the dataset powering CineMatch.'
        '</div>',
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(3, gap="medium")

    with metric_columns[0]:
        display_metric("MOVIES", f"{movie_count:,}")

    with metric_columns[1]:
        display_metric("USERS", f"{user_count:,}")

    with metric_columns[2]:
        display_metric("RATINGS", f"{rating_count:,}")

    st.markdown(
        '<div class="section-title">Three ways to discover</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        'Choose the recommendation approach that suits you.'
        '</div>',
        unsafe_allow_html=True,
    )

    feature_columns = st.columns(3, gap="medium")

    features = [
        (
            "👥",
            "User-Based",
            "Find movies liked by users with rating patterns "
            "similar to yours.",
        ),
        (
            "🎭",
            "Content-Based",
            "Explore movies with genres similar to a movie "
            "you already enjoy.",
        ),
        (
            "✨",
            "Hybrid",
            "Combine user preferences and movie characteristics "
            "in one recommendation approach.",
        ),
    ]

    for column, feature in zip(feature_columns, features):
        icon, title, description = feature

        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-description">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    st.markdown("### Ready to discover movies?")
    st.write(
        "Open Recommendations in the sidebar to choose a method "
        "and start exploring."
    )

    if st.button("Explore Recommendations", use_container_width=False):
        st.session_state["navigation_page"] = "Recommendations"
        st.rerun()


# =========================================================
# RECOMMENDATIONS PAGE
# =========================================================

elif page == "Recommendations":
    st.markdown(
        '<div class="eyebrow">PERSONALIZED DISCOVERY</div>',
        unsafe_allow_html=True,
    )
    st.title("Find your next favorite")
    st.markdown(
        '<div class="section-subtitle">'
        'Choose a recommendation method, adjust your options, '
        'and explore your results.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    method = st.selectbox(
        "Recommendation method",
        [
            "User-Based",
            "Content-Based",
            "Hybrid",
        ],
    )

    user_ids = sorted(ratings["userId"].unique().tolist())
    movie_options = movies[["movieId", "title"]].drop_duplicates()

    user_id = None

    if method in ["User-Based", "Hybrid"]:
        user_id = st.selectbox(
            "Select user",
            user_ids,
            format_func=lambda value: f"User {value}",
        )

    selected_movie_id = None

    if method in ["Content-Based", "Hybrid"]:
        search_query = st.text_input(
            "Search for a movie",
            placeholder="Type a movie title, e.g. Toy Story",
        ).strip()

        if search_query:
            matches = movie_options[
                movie_options["title"].str.contains(
                    search_query,
                    case=False,
                    na=False,
                    regex=False,
                )
            ]

            if matches.empty:
                st.warning("No matching movies found. Try another title.")
            else:
                st.caption(f"{len(matches)} matching movie(s) found.")

                selected_movie_id = st.selectbox(
                    "Choose a movie",
                    matches["movieId"].tolist(),
                    format_func=lambda movie_id: get_movie_title(movie_id),
                )
        else:
            st.info("Enter a movie title to choose a movie.")

    recommendation_count = st.slider(
        "Number of recommendations",
        min_value=5,
        max_value=20,
        value=10,
        step=5,
    )

    st.markdown("---")

    run_recommendations = st.button(
        "✨ Generate Recommendations",
        use_container_width=True,
    )

    if run_recommendations:
        if method == "Content-Based" and selected_movie_id is None:
            st.warning("Search for and select a movie first.")

        elif method == "Hybrid" and selected_movie_id is None:
            st.warning(
                "Hybrid recommendations require both a user "
                "and a selected movie."
            )

        else:
            try:
                with st.spinner("Finding movies for you..."):
                    if method == "User-Based":
                        results = recommend_movies(
                            int(user_id),
                            n=recommendation_count,
                        )

                    elif method == "Content-Based":
                        results = get_similar_movies(
                            int(selected_movie_id),
                            n=recommendation_count,
                        )

                    else:
                        results = get_hybrid_recommendations(
                            int(user_id),
                            int(selected_movie_id),
                            n=recommendation_count,
                        )

                display_recommendation_cards(results, method)

            except Exception as error:
                st.error("Something went wrong while generating recommendations.")
                st.code(str(error))


# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "About":
    st.markdown(
        '<div class="eyebrow">ABOUT THE PROJECT</div>',
        unsafe_allow_html=True,
    )
    st.title("About CineMatch")

    st.markdown(
        """
        <div class="hero">
            <h1>Movies you'll love.<br><span>Discovered differently.</span></h1>
            <p>
                CineMatch is a Python-based movie recommendation
                system built on the MovieLens dataset. It demonstrates
                three approaches to recommendation through one
                interactive application.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Technology stack")

    st.markdown(
        """
        - **Python** — core application and recommendation logic
        - **Pandas** — CSV loading and data preparation
        - **Scikit-learn** — similarity calculations in the recommendation pipeline
        - **Streamlit** — interactive web interface
        - **MovieLens CSV files** — movies, ratings, and links
        """
    )

    st.markdown("### Project architecture")

    st.code(
        """
MovieLens CSV files
        |
        v
src/data_loader.py
        |
        +--------------------+
        |                    |
        v                    v
User-Based             Content-Based
Filtering               Filtering
        |                    |
        +----------+---------+
                   |
                   v
          Hybrid Recommender
                   |
                   v
             Streamlit UI
        """,
        language="text",
    )

    st.markdown("### Project principles")

    st.write(
        "The current version uses local CSV files. It does not require "
        "a database or an external movie-data API."
    )

    st.caption("CineMatch · Built with Python and Streamlit")
