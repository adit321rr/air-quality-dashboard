import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filter Data")
station = st.sidebar.selectbox("Pilih Stasiun", df['station'].unique())

# Filter data berdasarkan stasiun yang dipilih
filtered_df = df[df['station'] == station]

# Main Dashboard
st.title(f"Dashboard Kualitas Udara: Stasiun {station}")

# Row 1: Metrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata PM2.5", f"{filtered_df['PM2.5'].mean():.2f}")
col2.metric("Nilai Maksimal PM2.5", f"{filtered_df['PM2.5'].max():.2f}")
col3.metric("Total Observasi", len(filtered_df))

st.markdown("---")

# Visualisasi 1: Menjawab Pertanyaan 1 (Tren)
st.subheader("1. Tren PM2.5 Bulanan (2013 - 2017)")
monthly_pm25 = filtered_df.resample('ME', on='datetime')['PM2.5'].mean().reset_index()
fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(data=monthly_pm25, x='datetime', y='PM2.5', marker='o', ax=ax, color='#1f77b4')
ax.set_ylabel("Rata-rata PM2.5")
ax.set_xlabel("Waktu")
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)

st.markdown("---")

# Visualisasi 2: Menjawab Pertanyaan 2 (Korelasi Suhu & PM2.5)
st.subheader("2. Hubungan Suhu Udara (TEMP) terhadap Polusi PM2.5")
st.write("Visualisasi ini menggunakan rata-rata harian untuk melihat pola korelasi dengan lebih jelas.")
# Resample ke harian agar scatter plot tidak terlalu berat dimuat di web
daily_df = filtered_df.resample('D', on='datetime')[['PM2.5', 'TEMP']].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=daily_df, x='TEMP', y='PM2.5', alpha=0.5, color='#d62728', ax=ax2)
ax2.set_title("Scatter Plot: Suhu vs PM2.5")
ax2.set_ylabel("Tingkat PM2.5")
ax2.set_xlabel("Suhu (Celcius)")
st.pyplot(fig2)

st.markdown("---")

# Visualisasi Lanjutan (Opsional untuk Bintang 5)
st.subheader("3. Proporsi Kategori Kualitas Udara (Berdasarkan PM2.5)")
def categorize_aqi(pm25):
    if pm25 <= 35: return 'Good'
    elif pm25 <= 75: return 'Moderate'
    elif pm25 <= 115: return 'Unhealthy for Sensitive Groups'
    elif pm25 <= 150: return 'Unhealthy'
    elif pm25 <= 250: return 'Very Unhealthy'
    else: return 'Hazardous'

filtered_df['AQI_Category'] = filtered_df['PM2.5'].apply(categorize_aqi)
cat_order = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous']

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.countplot(data=filtered_df, x='AQI_Category', order=cat_order, palette='viridis', ax=ax3)
plt.xticks(rotation=45)
ax3.set_ylabel("Jumlah Jam Observasi")
ax3.set_xlabel("Kategori")
st.pyplot(fig3)

st.caption("Copyright © Nasyrun Adetiya 2026")