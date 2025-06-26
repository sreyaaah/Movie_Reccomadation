import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

def load_data():
    """Load and merge ratings and movie data"""
    try:
        # Load ratings data
        ratings = pd.read_csv(
            'u.data', 
            sep='\t', 
            names=["user_id", "movie_id", "rating", "timestamp"],
            encoding='latin-1'
        )
        
        # Load movie titles
        movies = pd.read_csv(
            'u.item', 
            sep='|', 
            encoding='latin-1', 
            header=None, 
            usecols=[0, 1], 
            names=['movie_id', 'title']
        )
        
        # Merge and return
        return pd.merge(ratings, movies, on='movie_id')
    
    except FileNotFoundError:
        print("Error: Could not find data files (u.data and u.item)")
        return None
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def create_user_movie_matrix(data):
    """Create user-movie rating matrix"""
    if data is None:
        return pd.DataFrame()
    
    # Create pivot table and fill NaN with 0
    matrix = data.pivot_table(
        index='user_id', 
        columns='title', 
        values='rating'
    ).fillna(0)
    
    return matrix

def get_similar_movies(movie_name, user_movie_ratings, top_n=5):
    """Collaborative filtering using correlation"""
    if movie_name not in user_movie_ratings.columns:
        return []
    
    try:
        # Calculate correlations
        movie_ratings = user_movie_ratings[movie_name]
        similar_movies = user_movie_ratings.corrwith(movie_ratings)
        
        # Create and clean correlation dataframe
        corr_df = pd.DataFrame(similar_movies, columns=['Correlation'])
        corr_df.dropna(inplace=True)
        corr_df = corr_df[corr_df.index != movie_name]  # Remove self
        corr_df = corr_df.sort_values('Correlation', ascending=False)
        
        # Return top N recommendations
        return corr_df.head(top_n).index.tolist()
    
    except Exception as e:
        print(f"Error in collaborative filtering: {str(e)}")
        return []

def load_genre_features():
    """Load and prepare genre features for content-based filtering"""
    try:
        # Load movie data with genres
        movies_content = pd.read_csv(
            'u.item', 
            sep='|', 
            encoding='latin-1', 
            header=None
        )
        
        # Select relevant columns (movie_id, title, and 19 genre columns)
        movies_content = movies_content[[0, 1] + list(range(5, 24))]
        movies_content.columns = ['movie_id', 'title'] + [f'genre_{i}' for i in range(19)]
        
        # Set title as index and drop movie_id
        genre_features = movies_content.set_index('title').drop('movie_id', axis=1)
        
        return genre_features
    
    except Exception as e:
        print(f"Error loading genre features: {str(e)}")
        return pd.DataFrame()

def recommend_by_genre(movie_title, genre_features, top_n=5):
    """Content-based recommendations using genre similarity"""
    if movie_title not in genre_features.index:
        return []
    
    try:
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(
            [genre_features.loc[movie_title]], 
            genre_features
        )
        
        # Get top similar movies
        scores = list(enumerate(cosine_sim[0]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Skip the movie itself and get top N
        recommendations = []
        for i, (idx, score) in enumerate(scores):
            title = genre_features.index[idx]
            if title != movie_title:
                recommendations.append(title)
            if len(recommendations) >= top_n:
                break
                
        return recommendations
    
    except Exception as e:
        print(f"Error in content-based filtering: {str(e)}")
        return []

def find_close_matches(movie_name, available_movies, cutoff=0.6):
    """Find close matches for movie names"""
    matches = get_close_matches(
        movie_name, 
        available_movies, 
        n=1, 
        cutoff=cutoff
    )
    return matches 