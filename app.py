import requests
import streamlit as st
import pickle
import os

def download_file(url, filename):
    if not os.path.exists(filename):
        st.info(f"Downloading {filename}...")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        st.success(f"{filename} downloaded.")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=60b7a515176b5184f3c8c9426b676b19&language=en-US".format(
        movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

download_file(
    "https://drive.google.com/uc?export=download&id=1Ui87sVy5QpTBeZUdMVx7wdWTGNTyqIX4",
    "similarity.pkl"
)
st.title('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie to recommend",
    movies_list
)

if st.button('Show Recommendations'):
    movie_names, movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(movie_names[idx])
            st.image(movie_posters[idx])