import os
from dotenv import load_dotenv

load_dotenv()

TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")

TMDB_BASE_URL = "https://api.themoviedb.org/3"

TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"