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
st.sidebar.image("images1.png", use_container_width=True)
date_range = st.sidebar.date_input("Rentang Waktu", [pd.to_datetime("2011-01-01"), pd.to_datetime("2012-12-31")])
start_date = date_range[0].strftime("%Y-%m-%d")
end_date = date_range[1].strftime("%Y-%m-%d")
filtered_df = day_df.query(f'dteday >= "{start_date}" and dteday <= "{end_date}"')

# Header utama
st.markdown("# Bike Sharing ✨")
st.subheader("Daily Sharing")

# Metrics utama
total_sharing = filtered_df['cnt'].sum()
total_registered = filtered_df['registered'].sum()
total_casual = filtered_df['casual'].sum()
st.metric("Total Sharing Bike", f"{total_sharing:,}")
st.metric("Total Registered", f"{total_registered:,}")
st.metric("Total Casual", f"{total_casual:,}")

# Grafik pengaruh musim terhadap jumlah peminjaman
st.subheader("Bagaimana pengaruh musim terhadap jumlah peminjaman sepeda?")
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
sns.barplot(y="cnt", x="season", data=day_df.sort_values(by="season", ascending=False), palette=colors, ax=ax)
ax.set_title("Grafik Antar Musim", loc="center", fontsize=70)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# Grafik jam sibuk penyewaan sepeda
st.subheader("Kapan jam-jam sibuk dalam penyewaan sepeda?")
sum_order_items_df = hour_df.groupby('hr')['cnt'].sum().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={'hr': 'hours', 'cnt': 'count_cr'})
sum_order_items_df = sum_order_items_df.sort_values(by="count_cr", ascending=False)
sum_order_items_df['hours_label'] = sum_order_items_df['hours'].apply(lambda x: f"{x:02d}.00")
fig, ax = plt.subplots(figsize=(15, 8))
sns.barplot(x="hours_label", y="count_cr", data=sum_order_items_df.head(5), palette=["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax)
ax.set_xlabel("Jam (24-jam format)", fontsize=20)
ax.set_ylabel("Jumlah Peminjaman", fontsize=20)
ax.set_title("Jam Tersibuk Peminjaman Sepeda", fontsize=24)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
st.pyplot(fig)
