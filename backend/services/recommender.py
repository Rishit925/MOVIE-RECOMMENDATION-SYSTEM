import pickle
from pathlib import Path

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "models"

with open(MODEL_DIR / "movie_dict.pkl", "rb") as file:
    movie_dict = pickle.load(file)

with open(MODEL_DIR / "tfidf_vectors.pkl", "rb") as file:
    vectors = pickle.load(file)

with open(MODEL_DIR / "tfidf.pkl", "rb") as file:
    tfidf = pickle.load(file)

data = pd.DataFrame(movie_dict)

if len(data) != vectors.shape[0]:
    raise ValueError(
        "Number of movies and TF-IDF vectors do not match."
    )

def get_model_info():
    return {
        "movies": len(data),
        "features": vectors.shape[1],
        "vector_shape": list(vectors.shape)
    }

def search_movies(query: str, limit: int = 10):
    query = query.strip().lower()

    if not query:
        return []

    results = data[
        data["title"]
        .str.lower()
        .str.contains(query, na=False)
    ].head(limit)

    return [
        {
            "movie_id": int(row["movie_id"]),
            "title": row["title"]
        }
        for _, row in results.iterrows()
    ]

def get_movie_by_id(movie_id: int):
    matches = data[data["movie_id"] == movie_id]

    if matches.empty:
        return None

    row = matches.iloc[0]

    return {
        "movie_id": int(row["movie_id"]),
        "title": row["title"],
        "rating": round(float(row["vote_average"]), 1),
        "popularity": round(float(row["popularity"]), 2)
    }

def recommend_movies(movie_id: int, limit: int = 10):
    matches = data[data["movie_id"] == movie_id]

    if matches.empty:
        return None

    movie_index = matches.index[0]

    distance = cosine_similarity(
        vectors[movie_index],
        vectors
    ).flatten()

    # Get top 20 content-similar movies
    movie_list = sorted(
        list(enumerate(distance)),
        reverse=True,
        key=lambda x: x[1]
    )[1:21]

    recommendations = []

    for index, content_score in movie_list:

        rating_score = float(
            data.iloc[index]["rating_score"]
        )

        popularity_score = float(
            data.iloc[index]["popularity_score"]
        )

        # Hybrid recommendation score
        final_score = (
            0.75 * float(content_score)
            + 0.20 * rating_score
            + 0.05 * popularity_score
        )

        recommendations.append({
            "movie_id": int(data.iloc[index]["movie_id"]),
            "title": data.iloc[index]["title"],
            "similarity": round(float(content_score), 3),
            "rating": round(
                float(data.iloc[index]["vote_average"]), 1
            ),
            "popularity": round(
                float(data.iloc[index]["popularity"]), 2
            ),
            "score": round(final_score, 3)
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:limit]