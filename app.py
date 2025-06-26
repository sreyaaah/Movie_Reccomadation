import streamlit as st
from recommendation_logic import (
    load_data,
    create_user_movie_matrix,
    get_similar_movies,
    load_genre_features,
    recommend_by_genre,
    find_close_matches
)

# Configure page
st.set_page_config(page_title="Movie Recommendation System", layout="centered")
st.title("🎬 Movie Recommendation System")

# Load data once with caching
@st.cache_data
def setup():
    try:
        data = load_data()
        if data is None:
            return None, None
        user_movie_matrix = create_user_movie_matrix(data)
        genre_features = load_genre_features()
        return user_movie_matrix, genre_features
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        return None, None

user_movie_matrix, genre_features = setup()

# Only proceed if data loaded successfully
if user_movie_matrix is not None and genre_features is not None:
    # User input section
    st.subheader("🔍 Find Movie Recommendations")
    movie_name = st.text_input(
        "Enter a movie you like:", 
        placeholder="e.g. Star Wars (1977)",
        key="movie_input"
    )
    
    # Recommendation button
    if st.button("Get Recommendations", key="recommend_btn"):
        if not movie_name.strip():
            st.warning("Please enter a movie name.")
        else:
            with st.spinner("Finding recommendations..."):
                try:
                    # Check if exact match exists
                    if movie_name not in user_movie_matrix.columns:
                        matches = find_close_matches(movie_name, user_movie_matrix.columns)
                        if matches:
                            movie_name = matches[0]
                            st.info(f"Using closest match: {movie_name}")
                        else:
                            st.error(f"Movie '{movie_name}' not found. Please check spelling and include year.")
                            st.stop()
                    
                    # Display recommendations in tabs
                    tab1, tab2 = st.tabs(["Collaborative Filtering", "Content-Based"])
                    
                    with tab1:
                        st.subheader("🎯 Collaborative Recommendations")
                        sim_movies = get_similar_movies(movie_name, user_movie_matrix)
                        if sim_movies:
                            for i, movie in enumerate(sim_movies, 1):
                                st.markdown(f"{i}. {movie}")
                        else:
                            st.info("No collaborative recommendations found.")
                    
                    with tab2:
                        st.subheader("📊 Genre-Based Recommendations")
                        genre_recs = recommend_by_genre(movie_name, genre_features)
                        if genre_recs:
                            for i, movie in enumerate(genre_recs, 1):
                                st.markdown(f"{i}. {movie}")
                        else:
                            st.info("No genre-based recommendations found.")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Data load failed message
else:
    st.error("Failed to load data. Please check if data files (u.data and u.item) are in the correct location.")