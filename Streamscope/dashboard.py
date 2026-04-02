import streamlit as st
import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")

st.title("Netflix Content Analysis Dashboard")

df = pd.read_csv("Streamscope/netflix_cleaned_v2.csv")
st.title("📺 Netflix Data Dashboard")

total_titles = len(df)
total_movies = len(df[df['type'] == 'Movie'])
total_shows = len(df[df['type'] == 'TV Show'])

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", total_movies)
col3.metric("TV Shows", total_shows)

st.sidebar.header("Filters")

content_type = st.sidebar.selectbox(
    "Select Content Type",
    ["All", "Movie", "TV Show"]
)

if content_type != "All":
    df = df[df["type"] == content_type]

st.write("Dataset Shape:", df.shape)
st.dataframe(df.head())

st.subheader("Content Release Trend")

fig1 = px.histogram(
    df,
    x="release_year",
    title="Distribution of Netflix Content by Release Year"
)

st.plotly_chart(fig1)
st.subheader("Movies vs TV Shows Distribution")

fig2 = px.pie(
    df,
    names="type",
    title="Distribution of Movies and TV Shows on Netflix"
)

st.plotly_chart(fig2)
st.subheader("Top Genres on Netflix")

# Split genres and count
genres = df['listed_in'].str.split(',', expand=True).stack().str.strip()

top_genres = genres.value_counts().head(10)

fig3 = px.bar(
    x=top_genres.values,
    y=top_genres.index,
    orientation='h',
    title="Top 10 Genres on Netflix",
    labels={'x': 'Number of Titles', 'y': 'Genre'}
)

st.plotly_chart(fig3)

st.subheader("Movie Duration Distribution")

# Extract movie duration
movies = df[df['type'] == 'Movie']

movies['duration_int'] = pd.to_numeric(
    movies['duration'].str.replace(' min', ''),
    errors='coerce'
)

fig4 = px.histogram(
    movies,
    x="duration_int",
    nbins=30,
    title="Distribution of Movie Durations"
)

st.plotly_chart(fig4)
