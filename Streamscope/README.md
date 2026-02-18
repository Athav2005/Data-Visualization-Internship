# StreamScope - Netflix Content Strategy Analyzer

## Milestone 1: Dataset Preparation

### Objective
The goal of Milestone 1 is to prepare the Netflix Movies and TV Shows dataset for analysis by performing data cleaning and preprocessing.

### Dataset Information
- Source: Kaggle Netflix Movies and TV Shows Dataset
- Total Records: 8807
- Columns: 12 (expanded to 13 after feature engineering)

### Tasks Completed
1. Loaded the dataset using pandas.
2. Checked and identified missing values.
3. Removed duplicate records.
4. Handled missing values:
   - Replaced missing categorical values (director, cast, country, duration) with "Unknown".
   - Filled missing rating values using mode.
   - Converted `date_added` to datetime format.
5. Created a new derived feature: `year_added`.
6. Normalized categorical columns by removing extra spaces.
7. Exported the cleaned dataset as `netflix_cleaned.csv`.

### Result
The dataset is fully cleaned with no missing values and is ready for Exploratory Data Analysis (Milestone 2).

---

### Output File
- netflix_cleaned.csv (cleaned dataset)
