import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Netflix Smart Explorer", layout="wide")

# =========================
# 🎨 NETFLIX UI + ANIMATION
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(-45deg, #0f0f0f, #1c1c1c, #141414, #000000);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    color: white;
}

/* Netflix red glow */
h1, h2, h3 {
    color: #e50914;
    text-shadow: 0px 0px 10px rgba(229,9,20,0.7);
}

/* Hover cards */
.card {
    background-color: #1c1c1c;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 20px rgba(229,9,20,0.6);
}

/* Fade animation */
.fade-in {
    animation: fadeInUp 0.8s ease-in-out;
}

@keyframes fadeInUp {
    from {opacity: 0; transform: translateY(30px);}
    to {opacity: 1; transform: translateY(0px);}
}

@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

</style>
""", unsafe_allow_html=True)

st.title("🎬 Netflix Smart Content Explorer")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("Streamscope/netflix_cleaned_v2.csv")

df = load_data()

# =========================
# 🔝 TOP CONTROLS
# =========================
st.subheader("🎯 Find What to Watch")

col1, col2, col3 = st.columns(3)

with col1:
    mood = st.selectbox("Mood", ["Relax 😌", "Thrill 😈", "Family 👨‍👩‍👧", "Binge 📺"])

with col2:
    time_limit = st.slider("Max Duration (min)", 30, 180, 120)

with col3:
    surprise = st.button("🎉 Surprise Me")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Advanced Filters")
if st.sidebar.button("❌ Clear All Filters"):
    st.rerun()

type_filter = st.sidebar.multiselect("Type", df['type'].unique())
country_filter = st.sidebar.multiselect("Country", df['country'].dropna().unique())
rating_filter = st.sidebar.multiselect("Rating", df['rating'].dropna().unique())

# Genre filter
all_genres = df['listed_in'].dropna().str.split(',', expand=True).stack().str.strip().unique()
genre_filter = st.sidebar.multiselect("Genre", sorted(all_genres))

year_filter = st.sidebar.slider(
    "Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2000, 2020)
)

# =========================
# FILTER LOGIC
# =========================
filtered_df = df.copy()

if type_filter:
    filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]

if country_filter:
    filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]

if rating_filter:
    filtered_df = filtered_df[filtered_df['rating'].isin(rating_filter)]

if genre_filter:
    filtered_df = filtered_df[
        filtered_df['listed_in'].str.contains('|'.join(genre_filter), case=False, na=False)
    ]

filtered_df = filtered_df[
    (filtered_df['release_year'] >= year_filter[0]) &
    (filtered_df['release_year'] <= year_filter[1])
]

# =========================
# LOADING EFFECT
# =========================
with st.spinner("Updating dashboard..."):
    st.progress(100)
    time.sleep(0.3)

# =========================
# KPI
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

# =========================
# 🎉 SURPRISE
# =========================
if surprise:
    pick = df.sample(1).iloc[0]
    st.success(f"🎬 Try watching: {pick['title']}")
    st.balloons()

# =========================
# 🎬 MOOD MAP
# =========================
mood_map = {
    "Relax 😌": ["Drama", "Romantic", "Comedy"],
    "Thrill 😈": ["Action", "Thriller", "Crime"],
    "Family 👨‍👩‍👧": ["Children", "Family"],
    "Binge 📺": ["TV Shows"]
}

mood_genres = mood_map[mood]

# =========================
# CHARTS
# =========================
colA, colB = st.columns(2)

with colA:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    fig1 = px.histogram(filtered_df, x="release_year")
    fig1.update_layout(transition_duration=800)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    genres = filtered_df['listed_in'].str.split(',', expand=True).stack().str.strip()
    top_genres = genres.value_counts().head(10)
    fig2 = px.bar(x=top_genres.values, y=top_genres.index, orientation='h')
    fig2.update_layout(transition_duration=800)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    fig3 = px.pie(filtered_df, names="type")
    fig3.update_layout(transition_duration=800)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    movies = filtered_df[filtered_df['type'] == 'Movie'].copy()
    movies['duration_int'] = pd.to_numeric(
        movies['duration'].str.replace(' min', ''), errors='coerce'
    )
    movies = movies[movies['duration_int'] <= time_limit]

    fig4 = px.histogram(movies, x="duration_int")
    fig4.update_layout(transition_duration=800)
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# INSIGHTS
# =========================
st.markdown('<div class="fade-in">', unsafe_allow_html=True)

top_countries = filtered_df['country'].value_counts().head(10)
fig_country = px.bar(x=top_countries.values, y=top_countries.index, orientation='h')
fig_country.update_layout(transition_duration=800)
st.plotly_chart(fig_country, use_container_width=True)

growth = filtered_df.groupby('release_year').size().reset_index(name='count')
fig_growth = px.line(growth, x='release_year', y='count', markers=True)
fig_growth.update_layout(transition_duration=800)
st.plotly_chart(fig_growth, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 🎯 RECOMMENDATION (CARDS)
# =========================
st.subheader("🎯 Recommended For You")

rec = df[df['listed_in'].str.contains('|'.join(mood_genres), case=False, na=False)]

if not rec.empty:
    for _, row in rec.sample(min(5, len(rec))).iterrows():
        st.markdown(f"""
        <div class="card">
            <h4>🎬 {row['title']}</h4>
            <p>📅 {row['release_year']} | 🎭 {row['listed_in']}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================
# 🔎 SEARCH (CARDS)
# =========================
st.subheader("🔎 Search")

query = st.text_input("Search title")

if query:
    results = df[df['title'].str.contains(query, case=False, na=False)]

    for _, row in results.head(5).iterrows():
        st.markdown(f"""
        <div class="card">
            <h4>🎬 {row['title']}</h4>
            <p>{row['type']} | {row['release_year']}</p>
            <p>{row['listed_in']}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================
# DATA
# =========================
with st.expander("📊 View Data"):
    st.dataframe(filtered_df.head(50))