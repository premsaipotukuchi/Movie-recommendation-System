from http.client import responses
import pandas as pd
import streamlit as st  # Shortened alias for Streamlit
import pickle as pk
import requests

def fetch_poster(movie_id):
    """Fetch movie poster URL using TMDB API."""
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d991d71619851eeaf1d6a6ff1e4d63d4'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/150"  # Placeholder image for missing posters

def recommend(movie):
    """Recommend movies and fetch their posters."""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pk.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pk.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('🎬 Movie Recommender')
st.markdown(
    """
    **Discover your next favorite movie!**  
    Simply select a movie from the dropdown, and get personalized recommendations.
    """
)

# Movie selection
selected_movie_name = st.selectbox(
    'Search for your favorite movies:',
    movies['title'].values
)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)

    # Display recommendations
    st.markdown("### Recommended Movies")
    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, caption=name)

st.markdown(
    """
    ---
    *Built with ❤️ and powered by [TMDB API](https://www.themoviedb.org/documentation/api).*
    """
)
