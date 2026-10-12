import pandas as pd


MOVIES_FILES = "data/ml-latest-small/movies.csv"
RATINGS_FILES = "data/ml-latest-small/ratings.csv"
LINKS_FILES = "data/ml-latest-small/links.csv"


def load_movies():
    movies = pd.read_csv(MOVIES_FILES)
    return movies

def load_ratings():
    ratings = pd.read_csv(RATINGS_FILES)
    return ratings

def load_links():
    links = pd.read_csv(LINKS_FILES)
    return links



def prepare_movies():
    movies = load_movies()
    links = load_links()

    movies = movies.merge(
        links,
        on="movieId",
        how="left"
    )
    return movies


def prepare_ratings():
    ratings = load_ratings()

    ratings = ratings[
        ["userId", "movieId", "rating"]
    ]
    return ratings



def create_rating_matrix(ratings_df=None):
    if ratings_df is None:
        ratings_df = prepare_ratings()

    rating_matrix = ratings_df.pivot(
        index="userId",
        columns="movieId",
        values="rating"
    )

    rating_matrix = rating_matrix.fillna(0)

    return rating_matrix


