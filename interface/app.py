import streamlit as st
import pickle
import pandas as pd
import requests
import re

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=6d66085f3fa45ba5d821fd264baa6dac')
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data.get('poster_path', '')
    except:
        return ""

def load_collab_data():
    with open('/Users/nandanpatel/Projects/Movie Recomendation System/Colaborative Filtering/dataset/movies.pkl', 'rb') as f:
        movies = pickle.load(f)
    with open('/Users/nandanpatel/Projects/Movie Recomendation System/Colaborative Filtering/dataset/final.pkl', 'rb') as f:
        final = pickle.load(f)
    with open('/Users/nandanpatel/Projects/Movie Recomendation System/Colaborative Filtering/dataset/csr_data.pkl', 'rb') as f:
        csr_data = pickle.load(f)
    with open('/Users/nandanpatel/Projects/Movie Recomendation System/Colaborative Filtering/dataset/knn_model.pkl', 'rb') as f:
        knn = pickle.load(f)
    links = pd.read_csv('/Users/nandanpatel/Projects/Movie Recomendation System/Colaborative Filtering/dataset/links.csv')
    return movies, final, csr_data, knn, links

def get_recommendation_collaborative(movie_name, movies, final, csr_data, knn, links):
    movie_list = movies[movies['title'].str.contains(movie_name, case=False, na=False)]
    if len(movie_list):
        movie_id = movie_list.iloc[0]['movieId']
        try:
            final_idx = final[final['movieId'] == movie_id].index[0]
        except IndexError:
            return []

        distance, indices = knn.kneighbors(csr_data[final_idx], n_neighbors=11)
        rec_movies = sorted(list(zip(indices.squeeze().tolist(), distance.squeeze().tolist())),
                            key=lambda x: x[1])[1:]  # exclude self

        recommended = []
        for val in rec_movies:
            rec_movie_id = final.loc[val[0]]['movieId']
            idx = movies[movies['movieId'] == rec_movie_id].index
            title = movies.iloc[idx]['title'].values[0]
            tmdb_row = links[links['movieId'] == rec_movie_id]
            tmdb_id = tmdb_row['tmdbId'].values[0] if not tmdb_row.empty else None
            poster_url = fetch_poster(tmdb_id) if tmdb_id else ""
            recommended.append((title, poster_url))
        return recommended
    else:
        return []

def load_content_data():
    movies_df = pickle.load(open('/Users/nandanpatel/Projects/Movie Recomendation System/Content based/dataset/movies.pkl', 'rb'))
    similarity = pickle.load(open('/Users/nandanpatel/Projects/Movie Recomendation System/Content based/dataset/similarity.pkl', 'rb'))
    return pd.DataFrame(movies_df), similarity

def recommend_content(movie, movies_df, similarity):
    recommended = []
    posters = []
    try:
        index = movies_df[movies_df['title'] == movie].index[0]
    except IndexError:
        return [], []

    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended.append(movies_df.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended, posters

st.title("🎥 Movie Recommendation System")

# Select Recommendation Strategy
option = st.radio("Choose Recommendation Approach:", ["Collaborative Filtering", "Content Based Filtering"])

if option == "Collaborative Filtering":
    movies, final, csr_data, knn, links = load_collab_data()
    filtered_movies = movies[movies['movieId'].isin(final['movieId'])]
    movie_title = st.selectbox(
        "Select a movie to get recommendations:",
        options=["-- Select a movie --"] + sorted(filtered_movies['title'].unique())
    )

    if movie_title != "-- Select a movie --":
        st.success(f"You selected: **{movie_title}**")
        clean_title = re.sub(r"\s*\([^)]*\)", "", movie_title)
        recommendations = get_recommendation_collaborative(clean_title, movies, final, csr_data, knn, links)

        if recommendations:
            st.subheader("Recommended Movies:")
            for title, poster in recommendations:
                cols = st.columns([1, 4])
                with cols[0]:
                    st.image(poster if poster else "", width=80)
                with cols[1]:
                    st.markdown(f"**{title}**")
        else:
            st.warning("No recommendations found for this movie.")

elif option == "Content Based Filtering":
    movies_df, similarity = load_content_data()

    movie_title = st.selectbox(
        "Select a movie to get recommendations:",
        options=["-- Select a movie --"] + sorted(movies_df['title'].unique())
    )

    if movie_title != "-- Select a movie --":
        st.success(f"You selected: **{movie_title}**")
        rec, posters = recommend_content(movie_title, movies_df, similarity)

        st.subheader("Recommended Movies:")
        for title, poster_url in zip(rec, posters):
            cols = st.columns([1, 4])
            with cols[0]:
                if poster_url:
                    st.image(poster_url, width=80)
                else:
                    st.write("🎬")
            with cols[1]:
                st.markdown(f"**{title}**")
    else:
        st.warning("Please select a valid movie to get recommendations.")

