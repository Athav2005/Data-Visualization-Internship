import pandas as pd

print("========== STREAMSCOPE - MILESTONE 1 ==========\n")

# Load Dataset
print("Loading Netflix dataset...")
df = pd.read_csv("data/netflix_titles.csv")

print("\nOriginal Dataset Shape:", df.shape)
print("\nMissing Values Before Cleaning:\n")
print(df.isnull().sum())

# Remove Duplicates
df = df.drop_duplicates()

# Handle Missing Values
df['director'] = df['director'].fillna("Unknown")
df['cast'] = df['cast'].fillna("Unknown")
df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
df['duration'] = df['duration'].fillna("Unknown")

# Convert and Fix Date
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['date_added'] = df['date_added'].fillna(pd.Timestamp("2000-01-01"))
df['year_added'] = df['date_added'].dt.year

# Normalize Categorical Columns
df['country'] = df['country'].str.strip()
df['rating'] = df['rating'].str.strip()
df['listed_in'] = df['listed_in'].str.strip()

print("\nMissing Values After Cleaning:\n")
print(df.isnull().sum())

print("\nFinal Dataset Shape:", df.shape)

# Save Cleaned Dataset
df.to_csv("netflix_cleaned.csv", index=False)

print("\nDataset successfully cleaned and saved as 'netflix_cleaned.csv'")
print("\n========== MILESTONE 1 COMPLETED ==========")
