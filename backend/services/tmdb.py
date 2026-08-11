import requests
from functools import lru_cache

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from backend.core.config import (
    TMDB_READ_ACCESS_TOKEN,
    TMDB_BASE_URL,
    TMDB_IMAGE_BASE_URL
)


# --------------------------------------------------
# HTTP session with retry support
# --------------------------------------------------

retry_strategy = Retry(
    total=3,
    connect=3,
    read=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(
    max_retries=retry_strategy
)

session = requests.Session()

session.mount(
    "https://",
    adapter
)

session.headers.update({
    "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
    "accept": "application/json",
    "User-Agent": "MovieRecommendationSystem/1.0"
})


# --------------------------------------------------
# Get movie details from TMDB
# --------------------------------------------------

@lru_cache(maxsize=500)
def get_movie_details(movie_id: int):

    if not TMDB_READ_ACCESS_TOKEN:
        raise ValueError(
            "TMDB Read Access Token is not configured."
        )

    url = f"{TMDB_BASE_URL}/movie/{movie_id}"

    response = session.get(
        url,
        timeout=(5, 15)
    )

    print(
        f"TMDB request: movie_id={movie_id}, "
        f"status={response.status_code}"
    )

    if response.status_code != 200:

        print(
            "TMDB response:",
            response.text
        )

        return None

    movie = response.json()

    poster_path = movie.get("poster_path")

    poster_url = None

    if poster_path:
        poster_url = (
            f"{TMDB_IMAGE_BASE_URL}"
            f"{poster_path}"
        )

    backdrop_url = None

    if movie.get("backdrop_path"):
        backdrop_url = (
            "https://image.tmdb.org/t/p/w1280"
            f"{movie['backdrop_path']}"
        )

    return {
        "tmdb_id": movie.get("id"),
        "title": movie.get("title"),
        "poster_url": poster_url,
        "backdrop_url": backdrop_url
    }