import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
cuaca_df_cleaned = pd.read_csv("cuaca_df_cleaned.csv")
musim_df_cleaned = pd.read_csv("musim_df_cleaned.csv")
waktu_puncak_df_cleaned = pd.read_csv("waktu_puncak_df_cleaned.csv")

# Map for readable weather and season names
weather_map = {1: 'Clear/Cloudy', 2: 'Misty', 3: 'Light Snow/Rain', 4: 'Heavy Snow/Rain'}
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

# Replace weather and season with readable names
cuaca_df_cleaned['weathersit'] = cuaca_df_cleaned['weathersit'].map(weather_map)
musim_df_cleaned['season'] = musim_df_cleaned['season'].map(season_map)

# Sidebar widget for filtering data
with st.sidebar:

    st.image("logobike.jpg")  
    st.title("Bike Rental Analysis Dashboard")
    
    # Date filters for hourly peak time
    selected_hour = st.slider('Select Hour', min_value=int(waktu_puncak_df_cleaned['hr'].min()), 
                              max_value=int(waktu_puncak_df_cleaned['hr'].max()), value=int(waktu_puncak_df_cleaned['hr'].median()))
    
    # Filtered data based on selected hour
    filtered_waktu_df = waktu_puncak_df_cleaned[waktu_puncak_df_cleaned['hr'] == selected_hour]
    
    # Season selection
    selected_season = st.selectbox("Select Season", musim_df_cleaned['season'].unique())
    filtered_musim_df = musim_df_cleaned[musim_df_cleaned['season'] == selected_season]

# Main Dashboard
st.title("Interactive Bike Rental Data Analysis")

# 1. Weather and Bike Rentals
st.subheader("Impact of Weather Conditions on Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=cuaca_df_cleaned, ax=ax)
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# 2. Season and Rentals
st.subheader(f"Bike Rentals in {selected_season}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='yr', y='cnt', data=filtered_musim_df, marker='o', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# 3. Peak Hours and Rentals
st.subheader(f"Bike Rentals at Hour {selected_hour}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', hue='workingday', data=filtered_waktu_df, ax=ax)
ax.set_xlabel("Weekday")
ax.set_ylabel("Number of Rentals")
st.pyplot(fig)

# Conclusion based on the data
st.write("""
### Conclusion:
- Weather: Clear/Cloudy conditions have the highest bike rental counts, while bad weather (heavy snow/rain) reduces rentals.
- Season: Rentals fluctuate between seasons, with the selected season showing unique patterns in each year.
- Peak Hours: The chosen hour shows notable differences between weekdays and weekends, as well as working and non-working days.
""")
