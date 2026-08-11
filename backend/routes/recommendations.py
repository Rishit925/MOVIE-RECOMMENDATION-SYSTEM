from fastapi import APIRouter, HTTPException

from backend.services.recommender import (
    get_movie_by_id,
    recommend_movies
)

from backend.services.tmdb import get_movie_details


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/{movie_id}")
def recommend(movie_id: int):

    # ---------------------------------------------
    # Get selected movie
    # ---------------------------------------------

    movie = get_movie_by_id(movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # ---------------------------------------------
    # Get ML recommendations
    # ---------------------------------------------

    recommendations = recommend_movies(movie_id)

    if recommendations is None:
        raise HTTPException(
            status_code=404,
            detail="Could not generate recommendations"
        )

    # ---------------------------------------------
    # Add selected movie poster
    # ---------------------------------------------

    try:
        selected_tmdb = get_movie_details(movie_id)

        if selected_tmdb:
            movie["poster_url"] = selected_tmdb.get("poster_url")
        else:
            movie["poster_url"] = None

    except Exception as e:
        print(
            f"TMDB error for selected movie {movie_id}: {e}"
        )

        movie["poster_url"] = None

    # ---------------------------------------------
    # Add posters to recommendations
    # ---------------------------------------------

    for recommendation in recommendations:

        rec_movie_id = recommendation["movie_id"]

        try:
            tmdb_details = get_movie_details(rec_movie_id)

            if tmdb_details:
                recommendation["poster_url"] = (
                    tmdb_details.get("poster_url")
                )
            else:
                recommendation["poster_url"] = None

        except Exception as e:

            print(
                f"TMDB error for movie "
                f"{rec_movie_id}: {e}"
            )

            recommendation["poster_url"] = None

    # ---------------------------------------------
    # Final response
    # ---------------------------------------------

    return {
        "selected_movie": movie,
        "recommendations": recommendations
    }