import streamlit as st
import pickle
import requests
import os

# Read API key locally
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


BASE_DIR = os.path.dirname(__file__)   # project root on server
movies_path = os.path.join(BASE_DIR, "movies.pkl")
sim_path = os.path.join(BASE_DIR, "similarity.pkl")


# Load movies and similarity
movies = pickle.load(open('movies.pkl','rb'))
movies_lists = movies['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))

# Fetch poster
def fetch_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    data = requests.get(url).json()
    try:
        poster_path = data['results'][0]['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    except:
        return None
    


# Recommendation function
def recommend(movie):
    movies_indx = int(movies[movies['title'] == movie].index[0])
    distances = similarity[movies_indx]
    recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    names = []
    posters = []
    
    for i in recommended_movies:
        movie_title = movies.iloc[i[0]].title
        names.append(movie_title)
        posters.append(fetch_poster(movie_title))
        
    return names, posters

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("MOVIE RECOMMENDATION SYSTEM")

select_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies_lists
)


if st.button("Recommend"):
    names, posters = recommend(select_movie_name)

    # Display 5 recommended movies in a single row
    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        
        if poster:
            col.image(poster)
        else:
            col.text("Poster not found")
        col.text(name)    

