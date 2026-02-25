import pandas as pd
from datetime import datetime

print("========== STREAMSCOPE - MILESTONE 1 ==========\n")

# -------------------- LOAD DATA --------------------

print("Loading Netflix dataset...")
df = pd.read_csv("data/netflix_titles.csv")

print("\nOriginal Dataset Shape:", df.shape)
print("\nMissing Values Before Cleaning:\n")
print(df.isnull().sum())

# -------------------- BASIC CLEANING --------------------

# Remove duplicates and reset index
df = df.drop_duplicates().reset_index(drop=True)

# Handle missing values
df['director'] = df['director'].fillna("Unknown")
df['cast'] = df['cast'].fillna("Unknown")
df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
df['duration'] = df['duration'].fillna("Unknown")

# Convert date column
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['date_added'] = df['date_added'].fillna(pd.Timestamp("2000-01-01"))

# Normalize categorical columns
df['country'] = df['country'].str.strip()
df['rating'] = df['rating'].str.strip().str.upper()
df['listed_in'] = df['listed_in'].str.strip()

# -------------------- FEATURE ENGINEERING --------------------

# 1️⃣ Year Added
df['year_added'] = df['date_added'].dt.year

# 2️⃣ Quarter Added
df['quarter_added'] = 'Q' + df['date_added'].dt.quarter.astype(str)

# 3️⃣ Duration (Numeric Extraction)
df['duration_int'] = df['duration'].str.extract('(\d+)')
df['duration_int'] = pd.to_numeric(df['duration_int'], errors='coerce')

# 4️⃣ Target Audience
def categorize_audience(rating):
    if rating in ['TV-Y', 'TV-Y7']:
        return 'Kids'
    elif rating in ['TV-G', 'PG']:
        return 'Family'
    elif rating in ['TV-PG', 'TV-14']:
        return 'Teens'
    elif rating in ['R', 'TV-MA']:
        return 'Adults'
    else:
        return 'Not Rated'

df['target_audience'] = df['rating'].apply(categorize_audience)

# 5️⃣ Content Age
current_year = datetime.now().year
df['content_age'] = current_year - df['release_year']

# 6️⃣ Added Delay
df['added_delay'] = df['year_added'] - df['release_year']

# 7️⃣ Genre Count
df['genre_count'] = df['listed_in'].str.split(', ').apply(len)

# 8️⃣ Multi-National Flag
df['is_multinational'] = df['country'].str.split(', ').apply(lambda x: len(x) > 1)

# -------------------- FINAL CHECK --------------------

print("\nMissing Values After Cleaning:\n")
print(df.isnull().sum())

print("\nFinal Dataset Shape:", df.shape)

# -------------------- SAVE CLEANED DATA --------------------

df.to_csv("netflix_cleaned_v2.csv", index=False)

print("\nDataset successfully cleaned and saved as 'netflix_cleaned_v2.csv'")
print("\n========== MILESTONE 1 COMPLETED ==========")