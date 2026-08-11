from fastapi import APIRouter, Query

from backend.services.recommender import search_movies


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/search")
def search(
    query: str = Query(
        ...,
        min_length=1,
        description="Movie title to search for"
    )
):
    return search_movies(query)