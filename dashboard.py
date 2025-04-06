import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("day_cleaned.csv")
hour_df = pd.read_csv("hour_cleaned.csv")

# Konfigurasi dashboard
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.markdown("""
    <style>
        .main {background-color: #0E1117; color: white;}
        div[data-testid="stSidebar"] {background-color: #161B22;}
    </style>
""", unsafe_allow_html=True)

# Sidebar dengan rentang waktu
st.sidebar.title("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", pd.to_datetime(day_df['dteday'].min()))
end_date = st.sidebar.date_input("Tanggal Akhir", pd.to_datetime(day_df['dteday'].max()))
selected_season = st.sidebar.multiselect("Pilih Musim", options=day_df['season'].unique(), default=day_df['season'].unique())

# Filter berdasarkan tanggal, musim, dan cuaca
filtered_day_df = day_df[
    (pd.to_datetime(day_df['dteday']) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(day_df['dteday']) <= pd.to_datetime(end_date)) &
    (day_df['season'].isin(selected_season))
]

# Header utama
st.markdown("# Bike Sharing ✨")
st.subheader("Daily Sharing")

# Metrics utama
total_sharing = filtered_day_df['cnt'].sum()
total_registered = filtered_day_df['registered'].sum()
total_casual = filtered_day_df['casual'].sum()
st.metric("Total Sharing Bike", f"{total_sharing:,}")
st.metric("Total Registered", f"{total_registered:,}")
st.metric("Total Casual", f"{total_casual:,}")

# Grafik pengaruh musim terhadap jumlah peminjaman
st.subheader("Bagaimana pengaruh musim terhadap jumlah peminjaman sepeda?")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
sns.barplot(y="cnt", x="season", data=filtered_day_df.sort_values(by="season", ascending=False), palette=colors, ax=ax)
ax.set_title("Grafik Antar Musim", loc="center", fontsize=70)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

#
st.subheader("Bagaimana distribusi tren penyewaan sepeda per bulan?")

# Tambahkan kolom bulan
filtered_day_df['dteday'] = pd.to_datetime(filtered_day_df['dteday'])
filtered_day_df['bulan'] = filtered_day_df['dteday'].dt.to_period('M').astype(str)

monthly_trend = filtered_day_df.groupby('bulan')['cnt'].sum().reset_index()


# Ambil 5 bulan dengan jumlah peminjaman tertinggi
top5_months = monthly_trend.sort_values(by='cnt', ascending=False).head(5)

fig3, ax3 = plt.subplots(figsize=(15, 8))
sns.barplot(x='bulan', y='cnt', data=top5_months, palette="Blues_d", ax=ax3)
ax3.set_xlabel("Bulan", fontsize=20)
ax3.set_ylabel("Jumlah Peminjaman", fontsize=20)
ax3.set_title("Top 5 Bulan dengan Jumlah Peminjaman Tertinggi", fontsize=24)
ax3.tick_params(axis='x', labelsize=16)
ax3.tick_params(axis='y', labelsize=16)
st.pyplot(fig3)
