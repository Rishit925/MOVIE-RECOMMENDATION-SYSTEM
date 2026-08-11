import streamlit as st
from pathlib import Path
import pandas as pd
import requests
import sys
import os


BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# PATHS & API CONFIGURATION
# ==========================================================

MOVIES_FILE = BASE_DIR / "tmdb_5000_movies.csv"

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://movie-recommender-backend-h1k5.onrender.com"
)


# ==========================================================
# LOAD MOVIE DATA
# ==========================================================

@st.cache_data
def load_movies():

    data = pd.read_csv(MOVIES_FILE)

    return data


try:

    movies = load_movies()

except Exception:

    st.error("Unable to load the movie dataset.")

    st.stop()

MOVIE_ID_COLUMN = (
    "movie_id"
    if "movie_id" in movies.columns
    else "id"
    )


# ==========================================================
# API REQUEST
# ==========================================================

def get_recommendations(movie_id):

    url = f"{API_BASE_URL}/recommendations/{movie_id}"

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
"""
<style>

/* ================================================== */
/* MAIN TITLES */
/* ================================================== */

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #9CA3AF;
    margin-bottom: 30px;
}


/* ================================================== */
/* HERO */
/* ================================================== */

.hero-box {
    padding: 30px;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 25px;
}


/* ================================================== */
/* FEATURE CARDS */
/* ================================================== */

.feature-card {
    padding: 22px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.25);
    min-height: 150px;
    transition: all 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    border-color: rgba(128,128,128,0.55);
}

.feature-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
}

.feature-text {
    font-size: 15px;
    color: #9CA3AF;
    line-height: 1.5;
}


/* ================================================== */
/* SIDEBAR */
/* ================================================== */

section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.20);
}

.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    line-height: 1.25;
    text-align: center;
    margin-bottom: 8px;
}


/* ================================================== */
/* MOVIE CARD */
/* ================================================== */

.movie-card {
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.25);
    height: 100%;
    transition: all 0.25s ease;
}

.movie-card:hover {
    transform: translateY(-5px);
    border-color: rgba(128,128,128,0.65);
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.movie-title {
    font-size: 18px;
    font-weight: 650;
    margin-top: 10px;
    margin-bottom: 8px;
}

.movie-meta {
    font-size: 14px;
    color: #AAAAAA;
    line-height: 1.7;
}


/* ================================================== */
/* SELECTED MOVIE */
/* ================================================== */

.selected-movie-box {
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,0.30);
    margin: 20px 0 30px 0;
}


/* ================================================== */
/* BUTTONS */
/* ================================================== */

div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}


/* ================================================== */
/* ABOUT PAGE */
/* ================================================== */

/* Project overview */

.about-card {
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.04);
    margin: 10px 0 30px 0;
}

.about-card p {
    font-size: 16px;
    line-height: 1.7;
    color: #D1D5DB;
    margin-bottom: 10px;
}

.about-card p:last-child {
    margin-bottom: 0;
}


/* How it works cards */

.about-step {
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    height: 250px;
    box-sizing: border-box;
    transition: all 0.25s ease;
}

.about-step:hover {
    transform: translateY(-5px);
    border-color: rgba(128,128,128,0.60);
    box-shadow: 0 8px 25px rgba(0,0,0,0.20);
}

.about-step h3 {
    font-size: 20px;
    margin: 12px 0 10px 0;
}

.about-step p {
    color: #9CA3AF;
    line-height: 1.6;
    font-size: 15px;
}


/* Number inside steps */

.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: rgba(99,102,241,0.15);
    font-size: 20px;
    font-weight: 700;
}


/* ================================================== */
/* RANKING CARDS */
/* ================================================== */

.ranking-card {
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    min-height: 175px;
    transition: all 0.25s ease;
}

.ranking-card:hover {
    transform: translateY(-4px);
    border-color: rgba(128,128,128,0.60);
}

.ranking-card h3 {
    font-size: 19px;
    margin-bottom: 12px;
}

.ranking-card p {
    color: #9CA3AF;
    line-height: 1.6;
    font-size: 15px;
}


/* ================================================== */
/* TECHNOLOGY CARDS */
/* ================================================== */

.tech-card {
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    min-height: 145px;
    transition: all 0.25s ease;
}

.tech-card:hover {
    transform: translateY(-5px);
    border-color: rgba(128,128,128,0.60);
    box-shadow: 0 8px 25px rgba(0,0,0,0.20);
}

.tech-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.tech-card h3 {
    font-size: 19px;
    margin: 5px 0;
}

.tech-card p {
    color: #9CA3AF;
    font-size: 14px;
}


/* ================================================== */
/* APPLICATION ARCHITECTURE */
/* ================================================== */

.architecture {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.04);
    margin-bottom: 30px;
}

.architecture-item {
    flex: 1;
    text-align: center;
    padding: 18px 10px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.20);
}

.architecture-item b {
    display: block;
    font-size: 17px;
    margin-bottom: 6px;
}

.architecture-item span {
    display: block;
    color: #9CA3AF;
    font-size: 13px;
}

.architecture-arrow {
    font-size: 25px;
    color: #9CA3AF;
}


/* ================================================== */
/* ABOUT FOOTER */
/* ================================================== */

.about-footer {
    text-align: center;
    padding: 25px;
    margin-top: 10px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.20);
}

.about-footer h3 {
    font-size: 17px;
    margin-bottom: 5px;
}

.about-footer p {
    color: #9CA3AF;
    font-size: 13px;
    margin: 0;
}


/* ================================================== */
/* GENERAL FOOTER */
/* ================================================== */

.footer {
    text-align: center;
    color: #B8B8C0;
    padding: 25px 0 10px 0;
    font-size: 14px;
    line-height: 1.8;
    margin-top: 20px;
}

.footer-tech {
    display: block;
    font-size: 12px;
    color: #777780;
    margin-top: 4px;
}

</style>
""",
unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
    """
    <div class="sidebar-title">
        Movie Recommendation<br>
        System
    </div>
    """,
    unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🧭 Navigation")
    st.caption("Select a section")

    if "page" not in st.session_state:
        st.session_state["page"] = "🏠 Home"


    if st.button(
        "🏠  Home",
        use_container_width=True
    ):
        st.session_state["page"] = "🏠 Home"


    if st.button(
        "🎯  Recommendations",
        use_container_width=True
    ):
        st.session_state["page"] = "🎯 Recommendations"


    if st.button(
        "ℹ️  About",
        use_container_width=True
    ):
        st.session_state["page"] = "ℹ️ About"


    page = st.session_state["page"]

    st.divider()

    st.markdown("### ⚙️ Settings")

    number_of_recommendations = st.slider(
        "Number of recommendations",
        min_value=5,
        max_value=10,
        value=5,
        step=5
    )

    show_ratings = st.toggle(
    "⭐ Show ratings",
    value=True
    )

    show_popularity = st.toggle(
    "🔥 Show popularity",
    value=True
    )

    show_score = st.toggle(
    "🎯 Show recommendation score",
    value=True
    )

    st.divider()

    st.caption(
        f"🎬 {len(movies):,} movies available"
    )

    st.caption(
        "Powered by FastAPI + Streamlit + TMDB"
    )


# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    # ------------------------------------------------------
    # HERO
    # ------------------------------------------------------

    st.markdown(
        """
        <div class="main-title">
            🎬 Discover Your Next Movie
        </div>

        <div class="subtitle">
            Find movies you'll love based on what you already enjoy.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 🍿 Popular Movies")

    st.caption(
    "Explore movies from our recommendation collection."
    )

    # ------------------------------------------------------
    # POPULAR MOVIE POSTERS
    # ------------------------------------------------------

    popular_movie_ids = [
    19995,   # Avatar
    155,     # The Dark Knight
    24428,   # The Avengers
    293660,  # Deadpool
    118340   # Guardians of the Galaxy
    ]

    poster_columns = st.columns(5)

    for column, movie_id in zip(poster_columns, popular_movie_ids):

        try:

            response = requests.get(
            f"{API_BASE_URL}/tmdb/{movie_id}",
            timeout=15
                )

            response.raise_for_status()

            movie_details = response.json()

            if movie_details:

                with column:

                    poster_url = movie_details.get("poster_url")
                    title = movie_details.get("title", "Movie")

                    if poster_url:

                        st.image(
                        poster_url,
                        use_container_width=True
                        )

                        st.markdown(
                        f"**{title}**"
                        )

                    else:

                        st.info("Poster unavailable.")

        except Exception as e:

            with column:
                st.warning("Unable to load movie.")


    # ------------------------------------------------------
    # HOW IT WORKS
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown("### ✨ How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 1️⃣ Choose a Movie")

        st.write(
            "Select a movie you already enjoy from the recommendation engine."
        )

    with col2:

        st.markdown("### 2️⃣ Find Similar Movies")

        st.write(
            "The system analyzes movie content and identifies titles "
            "with similar characteristics."
        )

    with col3:

        st.markdown("### 3️⃣ Get Recommendations")

        st.write(
            "Movies are ranked using content similarity, ratings and popularity."
        )



# ==========================================================
# RECOMMENDATION PAGE
# ==========================================================

elif page == "🎯 Recommendations":

    st.markdown(
        '<div class="main-title">🎯 Movie Recommendation System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Choose a movie and discover similar titles.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ------------------------------------------------------
    # MOVIE SELECTION
    # ------------------------------------------------------

    movie_options = (
        movies["title"]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
    )


    selected_title = st.selectbox(
        "🔎 Search and select a movie",
        movie_options,
        index=None,
        placeholder="Type a movie title..."
    )


    # ------------------------------------------------------
    # RECOMMEND BUTTON
    # ------------------------------------------------------

    recommend_button = st.button(
        "🎬 Get Recommendations",
        type="primary",
        use_container_width=True
    )


    if recommend_button:

        if selected_title is None:

            st.warning(
                "Please select a movie first."
            )

        else:

            # --------------------------------------------------
            # GET MOVIE ID
            # --------------------------------------------------

            selected_rows = movies[
                movies["title"] == selected_title
            ]

            if selected_rows.empty:

                st.error(
                    "Selected movie could not be found."
                )

            else:

                movie_id = int(
                    selected_rows.iloc[0]["id"]
                )


                # --------------------------------------------------
                # CALL FASTAPI
                # --------------------------------------------------

                try:

                    with st.spinner(
                        "Finding movies you might like..."
                    ):

                        result = get_recommendations(
                            movie_id
                        )


                    # Store result so it survives reruns
                    st.session_state["recommendation_result"] = result


                except requests.exceptions.ConnectionError:

                    st.error(
                        "🔴 Could not connect to the FastAPI backend. "
                        "Make sure Uvicorn is running on port 8000."
                    )


                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ The recommendation service took too long "
                        "to respond."
                    )


                except requests.exceptions.HTTPError as e:

                    st.error(
                        f"FastAPI returned an error: {e}"
                    )


                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


    # ------------------------------------------------------
    # DISPLAY STORED RESULT
    # ------------------------------------------------------

    if "recommendation_result" in st.session_state:

        result = st.session_state[
            "recommendation_result"
        ]

        selected_movie = result.get(
            "selected_movie"
        )

        recommendations = result.get(
            "recommendations",
            []
        )


        # ==================================================
        # SELECTED MOVIE
        # ==================================================

        if selected_movie:

            st.markdown(
                "### 🎬 Your Selected Movie"
            )

            selected_col1, selected_col2 = st.columns(
                [1, 3]
            )


            with selected_col1:

                poster_url = selected_movie.get(
                    "poster_url"
                )

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Poster unavailable"
                    )


            with selected_col2:

                st.markdown(
                    f"## {selected_movie.get('title', 'Unknown')}"
                )


                rating = selected_movie.get(
                    "rating"
                )

                popularity = selected_movie.get(
                    "popularity"
                )


                if show_ratings and rating is not None:

                    st.write(
                        f"⭐ **Rating:** {float(rating):.1f}"
                    )


                if show_popularity and popularity is not None:

                    st.write(
                        f"🔥 **Popularity:** "
                        f"{float(popularity):.2f}"
                    )


                st.caption(
                    "Recommendations are generated using "
                    "content similarity, ratings and popularity."
                )


        # ==================================================
        # RECOMMENDATIONS
        # ==================================================

        st.markdown(
            "### 🎯 Recommended For You"
        )


        recommendations = recommendations[
            :number_of_recommendations
        ]


        if not recommendations:

            st.info(
                "No recommendations were returned."
            )

        else:

            # Create 4 cards per row

            for start in range(
                0,
                len(recommendations),
                4
            ):

                row = recommendations[
                    start:start + 4
                ]

                columns = st.columns(
                    len(row)
                )


                for column, recommendation in zip(
                    columns,
                    row
                ):

                    with column:

                        poster_url = recommendation.get(
                            "poster_url"
                        )

                        if poster_url:

                            st.image(
                                poster_url,
                                use_container_width=True
                            )

                        else:

                            st.markdown(
                                """
                                <div style="
                                    height:280px;
                                    display:flex;
                                    align-items:center;
                                    justify-content:center;
                                    border-radius:12px;
                                    border:1px solid
                                    rgba(128,128,128,0.25);
                                ">
                                    🎬<br>
                                    Poster unavailable
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                        title = recommendation.get(
                            "title",
                            "Unknown"
                        )

                        st.markdown(
                            f"""
                            <div class="movie-title">
                            {title}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                        # ------------------------------------------
                        # METADATA
                        # ------------------------------------------

                        rating = recommendation.get(
                            "rating"
                        )

                        popularity = recommendation.get(
                            "popularity"
                        )

                        similarity = recommendation.get(
                            "similarity"
                        )

                        score = recommendation.get(
                            "score"
                        )


                        if show_ratings and rating is not None:

                            st.write(
                                f"⭐ {float(rating):.1f}"
                            )


                        if show_popularity and popularity is not None:

                            st.write(
                                f"🔥 {float(popularity):.2f}"
                            )


                        if similarity is not None:

                            st.write(
                                f"🧠 Similarity: "
                                f"{float(similarity):.3f}"
                            )


                        if show_score and score is not None:

                            st.write(
                                f"🎯 Score: "
                                f"{float(score):.3f}"
                            )


                        # ------------------------------------------
                        # DETAILS
                        # ------------------------------------------

                        with st.expander(
                            "ℹ️ Details"
                        ):

                            if rating is not None:

                                st.write(
                                    f"⭐ Rating: "
                                    f"{float(rating):.1f}"
                                )


                            if popularity is not None:

                                st.write(
                                    f"🔥 Popularity: "
                                    f"{float(popularity):.2f}"
                                )


                            if similarity is not None:

                                st.write(
                                    f"🧠 Content similarity: "
                                    f"{float(similarity):.3f}"
                                )


                            if score is not None:

                                st.write(
                                    f"🎯 Final score: "
                                    f"{float(score):.3f}"
                                )

                            st.caption(
                                "The recommendation score combines "
                                "content similarity, rating and popularity."
                            )

# ==========================================================
# ABOUT PAGE
# ==========================================================

if page == "ℹ️ About":

    st.markdown(
        '<div class="main-title">ℹ️ About the Project</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        An intelligent movie recommendation system that helps you
        discover movies similar to the ones you already enjoy.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # PROJECT OVERVIEW
    # ------------------------------------------------------

    st.markdown("### 🎬 What is this project?")

    st.markdown(
        """
        <div class="about-card">

        <p>
        This application uses a <b>content-based recommendation approach</b>
        to find movies that are similar to a movie selected by the user.
        </p>

        <p>
        Movie information is analyzed using machine learning, while
        ratings and popularity are used to improve the final ranking.
        Movie posters and additional information are retrieved from
        the <b>TMDB API</b>.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # HOW IT WORKS
    # ------------------------------------------------------

    st.markdown("### ⚙️ How Recommendations Work")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="about-step">

            <div class="step-number">1</div>

            <h3>Choose a Movie</h3>

            <p>
            Select a movie from the available movie collection.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="about-step">

            <div class="step-number">2</div>

            <h3>Find Similar Movies</h3>

            <p>
            The system compares movie content using TF-IDF
            representations and cosine similarity.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="about-step">

            <div class="step-number">3</div>

            <h3>Rank the Results</h3>

            <p>
            Similar movies are ranked using content similarity,
            ratings and popularity.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ------------------------------------------------------
    # RANKING SYSTEM
    # ------------------------------------------------------

    st.markdown("### 🏆 Recommendation Ranking")

    st.markdown(
        """
        <div class="about-card">

        <p>
        The recommendation engine does not rely only on content similarity.
        It combines multiple signals to produce more useful results.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    rank1, rank2, rank3 = st.columns(3)

    with rank1:
        st.markdown(
            """
            <div class="ranking-card">
            <h3>🧠 Content Similarity</h3>
            <p>
            Measures how similar the selected movie is to other movies
            based on their available content.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with rank2:
        st.markdown(
            """
            <div class="ranking-card">
            <h3>⭐ Movie Rating</h3>
            <p>
            Helps prioritize movies that have stronger user ratings.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with rank3:
        st.markdown(
            """
            <div class="ranking-card">
            <h3>🔥 Popularity</h3>
            <p>
            Helps surface movies that have attracted greater audience
            interest.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ------------------------------------------------------
    # TECHNOLOGY STACK
    # ------------------------------------------------------

    st.markdown("### 🛠️ Technology Stack")

    tech1, tech2, tech3, tech4 = st.columns(4)

    with tech1:
        st.markdown(
            """
            <div class="tech-card">
            <div class="tech-icon">🧠</div>
            <h3>Scikit-learn</h3>
            <p>TF-IDF & similarity</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech2:
        st.markdown(
            """
            <div class="tech-card">
            <div class="tech-icon">⚡</div>
            <h3>FastAPI</h3>
            <p>Recommendation API</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech3:
        st.markdown(
            """
            <div class="tech-card">
            <div class="tech-icon">🎨</div>
            <h3>Streamlit</h3>
            <p>Interactive interface</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech4:
        st.markdown(
            """
            <div class="tech-card">
            <div class="tech-icon">🎬</div>
            <h3>TMDB</h3>
            <p>Movie posters & metadata</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ------------------------------------------------------
    # PROJECT ARCHITECTURE
    # ------------------------------------------------------

    st.markdown("### 🔗 Application Architecture")

    st.markdown(
        """
        <div class="architecture">

        <div class="architecture-item">
        🎨 <b>Streamlit</b>
        <span>User Interface</span>
        </div>

        <div class="architecture-arrow">→</div>

        <div class="architecture-item">
        ⚡ <b>FastAPI</b>
        <span>Recommendation API</span>
        </div>

        <div class="architecture-arrow">→</div>

        <div class="architecture-item">
        🧠 <b>ML Engine</b>
        <span>Similarity & Ranking</span>
        </div>

        <div class="architecture-arrow">→</div>

        <div class="architecture-item">
        🎬 <b>TMDB</b>
        <span>Movie Data</span>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------



    st.markdown(
    """
    <div class="footer">
        🎬 Movie Recommendation System<br>
        <span class="footer-tech">
            Content-Based Recommendation • FastAPI • Streamlit • TMDB
        </span>
    </div>
    """,
    unsafe_allow_html=True
    )