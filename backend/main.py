from fastapi import FastAPI, HTTPException

from backend.services.recommender import get_model_info
from backend.routes.movies import router as movies_router
from backend.routes.recommendations import router as recommendations_router
from backend.services.tmdb import get_movie_details

app = FastAPI(
    title="Movie Recommendation API",
    description="AI-powered movie recommendation system",
    version="1.0.0"
)

app.include_router(movies_router)
app.include_router(recommendations_router)

@app.get("/")
def root():
    return {
        "message": "Movie Recommendation API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/model-info")
def model_info():
    return get_model_info()

@app.get("/tmdb/{movie_id}")
def tmdb_movie(movie_id: int):

    try:
        result = get_movie_details(movie_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Movie was not found on TMDB."
            )

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"TMDB connection failed: {str(e)}"
        )