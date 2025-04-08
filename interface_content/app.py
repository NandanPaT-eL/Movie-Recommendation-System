import streamlit as st
import pickle
import pandas as pd
import requests

movies_df = pickle.load(open('dataset/movies.pkl', 'rb'))
movies_df = pd.DataFrame(movies_df)
similarity = pickle.load(open('dataset/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6d66085f3fa45ba5d821fd264baa6dac'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend_content(movie):
    recommended = []
    movie_poster = []

    index = movies_df.loc[movies_df['title'] == movie].index[0]  # Correct indexing
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended.append(movies_df.iloc[i[0]].title)
        movie_poster.append(fetch_poster(movie_id))
    return recommended, movie_poster

st.title("Movie Recommendation System")
movie_selected = st.selectbox("Choose a movie", movies_df['title'].values)

if st.button("Recommend"):
    rec, poster = recommend_content(movie_selected)
    col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="bottom")

    with col1:
        st.text(rec[0])
        st.image(poster[0])

    with col2:
        st.text(rec[1])
        st.image(poster[1])

    with col3:
        st.text(rec[2])
        st.image(poster[2])

    with col4:
        st.text(rec[3])
        st.image(poster[3])

    with col5:
        st.text(rec[4])
        st.image(poster[4])

