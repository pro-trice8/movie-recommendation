# app.py
import json
import os
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details


# Load config relative to this file, fallback to environment variable
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "config.json")
config = {}
if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        config = {}

# OMDB api key: try env var first, then config file
OMDB_API_KEY = os.environ.get("OMDB_API_KEY") or config.get("OMDB_API_KEY")

# Treat obvious placeholders as not set
if OMDB_API_KEY:
    key_str = str(OMDB_API_KEY).strip()
    if key_str == "" or key_str.lower().startswith("your_") or key_str.lower() == "your_omdb_api_key":
        OMDB_API_KEY = None

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommender")

# If OMDB key is not provided, show a warning and skip calling OMDB
if not OMDB_API_KEY:
    st.warning(
        "OMDB API key is not set. Movie plots and posters will not be available. "
        "Set the `OMDB_API_KEY` environment variable or add it to `src/config.json`."
    )

# Using 'title' instead of 'song' now
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

if st.button("🚀 Recommend Similar Movies"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")
            for _, row in recommendations.iterrows():
                movie_title = row['title']
                # Only call OMDB when we have a valid API key
                if OMDB_API_KEY:
                    plot, poster = get_movie_details(movie_title, OMDB_API_KEY)
                else:
                    plot, poster = "N/A", "N/A"

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=100)
                        else:
                            st.write("❌ No Poster Found")
                    with col2:
                        st.markdown(f"### {movie_title}")
                        st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available_")
