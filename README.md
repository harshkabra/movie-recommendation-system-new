# CineMatch — Movie Recommendation System

CineMatch is a Python-based movie recommendation system built using the **MovieLens Latest Small dataset**. It provides personalized movie recommendations using multiple recommendation techniques and presents the results through a Streamlit web interface.

The project is designed as a practical recommendation-system project demonstrating data processing, similarity-based recommendation, content-based filtering, hybrid recommendation, evaluation, and interactive UI development.

---

## Features

- User-based collaborative filtering
- Content-based movie recommendation
- Hybrid recommendation system
- Movie search
- User selection
- Adjustable number of recommendations
- Interactive Streamlit interface
- Recommendation evaluation using Precision@10 and Recall@10
- CSV-based data processing
- Uses `movies.csv`, `ratings.csv`, and `links.csv`
- No database required
- No external movie API required
- Modular Python project structure

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data loading and data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Similarity calculations |
| Streamlit | Web interface |
| Git | Version control |
| GitHub | Source code hosting |

---

## Recommendation Techniques

### 1. User-Based Collaborative Filtering

User-based collaborative filtering recommends movies by finding users with similar rating patterns.

The system:

1. Creates a user-movie rating matrix.
2. Calculates similarity between users.
3. Finds users similar to the selected user.
4. Collects movies rated by similar users.
5. Removes movies already watched by the target user.
6. Calculates a similarity-weighted recommendation score.
7. Returns the highest-scoring movies.

This approach is based on the idea that users with similar preferences may enjoy similar movies.

---

### 2. Content-Based Filtering

Content-based filtering recommends movies based on movie characteristics.

CineMatch currently uses movie **genres** as the content feature.

For example, if a user selects a movie containing:

```text
Adventure | Animation | Children | Comedy | Fantasy
```

the system searches for other movies with similar genre information.

Cosine similarity is used to measure the similarity between movies.

---

### 3. Hybrid Recommendation

The hybrid recommender combines:

- User-based collaborative filtering
- Content-based filtering

This allows the system to consider both:

```text
User preferences
        +
Movie characteristics
        ↓
Hybrid recommendation
```

The goal is to provide recommendations that consider both the user's historical preferences and the characteristics of the selected movie.

---

## Dataset

CineMatch uses the **MovieLens Latest Small dataset**.

The project uses three CSV files:

### movies.csv

Contains movie information.

Main columns:

```text
movieId
title
genres
```

### ratings.csv

Contains user movie ratings.

Main columns:

```text
userId
movieId
rating
timestamp
```

### links.csv

Contains external identifiers associated with MovieLens movies.

Main columns:

```text
movieId
imdbId
tmdbId
```

Although CineMatch does not currently use an external movie API, `links.csv` is retained as part of the project data pipeline for future extensibility.

---

## Dataset Statistics

The current MovieLens dataset contains approximately:

```text
Movies: 9,742
Ratings: 100,836
Users: 610
Unique rated movies: 9,724
```

Rating range:

```text
Minimum rating: 0.5
Maximum rating: 5.0
Average rating: approximately 3.50
```

---

## Project Structure

```text
movie-recommendation-system/
│
├── app.py
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── recommender.py
│   ├── content_based.py
│   ├── hybrid_recommender.py
│   └── evaluation.py
│
├── test_recommendation.py
├── test_evaluation.py
│
├── data/
│   └── ml-latest-small/
│       ├── movies.csv
│       ├── ratings.csv
│       └── links.csv
│
└── venv/
```

---

## File Responsibilities

### `app.py`

Contains the Streamlit web application.

It provides:

- CineMatch interface
- Movie search
- Recommendation method selection
- User selection
- Recommendation count selection
- Recommendation results
- About section

---

### `main.py`

Provides the command-line interface for testing the recommendation system without Streamlit.

---

### `src/data_loader.py`

Responsible for:

- Loading movies
- Loading ratings
- Loading links
- Preparing movie data
- Preparing rating data
- Creating the user-movie rating matrix

---

### `src/recommender.py`

Contains the user-based collaborative filtering implementation.

---

### `src/content_based.py`

Contains the content-based recommendation implementation using movie genres and cosine similarity.

---

### `src/hybrid_recommender.py`

Combines user-based and content-based recommendation scores.

---

#### movie-recommendation-system-new
