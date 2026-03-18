import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page config
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
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

# Row 2: Visualisasi Tren
st.subheader("Tren PM2.5 Bulanan")
monthly_pm25 = filtered_df.resample('M', on='datetime')['PM2.5'].mean().reset_index()
fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(data=monthly_pm25, x='datetime', y='PM2.5', marker='o', ax=ax, color='#1f77b4')
ax.set_ylabel("Rata-rata PM2.5")
ax.set_xlabel("Waktu")
st.pyplot(fig)

st.caption("Copyright © Nasyrun Adetiya 2026")