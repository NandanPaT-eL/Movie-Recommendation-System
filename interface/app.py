import streamlit as st
import pickle
import pandas as pd

movies_df = pickle.load(open('dataset/movies.pkl', 'rb'))
movies_df = pd.DataFrame(movies_df)
similarity = pickle.load(open('dataset/similarity.pkl', 'rb'))

def recommend(movie):
    recommended = []
    index = movies_df.loc[movies_df['title'] == movie].index[0]  # Correct indexing
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movie_list:
        recommended.append(movies_df.iloc[i[0]].title)
    return recommended

st.title("Movie Recommendation System")
movie_selected = st.selectbox("Choose a movie", movies_df['title'].values)

if st.button("Recommend"):
    rec = recommend(movie_selected)
    for i in rec:
        st.write(i)
