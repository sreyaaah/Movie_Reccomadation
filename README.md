 Movie Recommendation System
 The Movie Recommendation System is a machine learning-based application designed to suggest personalized movie
 recommendations to users. By leveraging both collaborative filtering and content-based filtering techniques, the system
 provides accurate and diverse suggestions based on user preferences and movie characteristics. This project
 demonstrates the practical application of recommendation algorithms using real-world data from the MovieLens dataset.
 2. Abstract
 This project implements a hybrid recommendation system that combines:
 
 Collaborative Filtering: Recommends movies based on ratings patterns from similar users.
 
 Content-Based Filtering: Recommends movies with similar genres to those the user has enjoyed.
 
 Key features:- 
 Fuzzy matching for movie title inputs (e.g., 'Star Wars' -> 'Star Wars (1977)').
 - Streamlit-based interactive UI for seamless user experience.
 - - Caching for efficient data loading and faster recommendations.
   - 
 3. Tools Used

 Category Tools/Libraries
 
 ProgrammingPython 3.x
 
 Data ProcessingPandas, NumPy
 
 Machine LearningScikit-learn (cosine similarity)
 
 UI FrameworkStreamlit
 
 Data SourceMovieLens dataset (u.data, u.item)
 
 4. Steps Involved in Building the Project

 Phase 1: Data Preparation
 
 Dataset Loading:- Loaded u.data (ratings) and u.item (movie metadata) using Pandas.- Merged datasets on movie_id.
 
 Data Preprocessing:- Created a user-movie rating matrix (pivot table) for collaborative filtering.- Extracted genre features (19 binary columns) for content-based filtering.

 Phase 2: Algorithm Implementation
 
 Collaborative Filtering:
 
- Calculated Pearson correlations between movies using corrwith().
- Returned top 5 movies with the highest correlation scores.

 Content-Based Filtering:-
 Used cosine similarity to compare genre vectors.
- Ranked movies by similarity to the input movie?s genres.

 Hybrid Integration:
- Combined both approaches in a single Streamlit interface with tabs.

 Phase 3: UI Development

 Streamlit App:
 - Added text input for movie names with fuzzy matching.
 - Designed tabs for collaborative/content-based results.
- Included error handling for invalid inputs.
  
 Optimizations:
 - Cached data loading with @st.cache_data to reduce latency.
 -  Added loading spinners (st.spinner) for better UX.
   
 5. Conclusion
 6. 
 The Movie Recommendation System successfully demonstrates how machine learning can enhance user experience by
 providing personalized suggestions. Key achievements:
 Accuracy: Hybrid approach mitigates limitations of individual methods (e.g., cold-start problem).
 Usability: Intuitive UI allows users to explore recommendations effortlessly
