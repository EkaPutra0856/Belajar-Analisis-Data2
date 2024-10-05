import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi dasar
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load dataset utama (clean_day.csv)
day_data = pd.read_csv('clean_day.csv')

# Mengubah kolom date menjadi datetime
day_data['date'] = pd.to_datetime(day_data['date'])

# Sidebar untuk rentang tanggal
min_date = day_data['date'].min()
max_date = day_data['date'].max()

with st.sidebar:
    st.title("Bike Sharing Dashboard")

    # Filter rentang tanggal
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data sesuai dengan rentang tanggal
filtered_data = day_data[(day_data['date'] >= pd.to_datetime(start_date)) & 
                         (day_data['date'] <= pd.to_datetime(end_date))]

# Bagian utama dashboard
st.header("Bike Sharing Dashboard 🚴‍♂️")

# 1. Penyewaan Berdasarkan Musim
st.subheader("Rentals by Season")

# Mengubah season ke kategori dengan nama yang lebih deskriptif
filtered_data['season'] = filtered_data['season'].map({
    1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'
})

season_rentals = filtered_data.groupby('season')['total_rentals'].sum()

fig, ax = plt.subplots(figsize=(10, 6))
season_rentals.plot(kind='bar', color='#90CAF9', ax=ax)
ax.set_xlabel("Season")
ax.set_ylabel("Total Bike Rentals")
ax.set_title("Total Bike Rentals by Season")
st.pyplot(fig)

# Deskripsi gambar
st.markdown("""
**Kesimpulan Grafik Penyewaan Berdasarkan Musim**:  
Musim panas memiliki jumlah penyewaan sepeda tertinggi, sementara musim dingin paling rendah. Hal ini menunjukkan pengaruh signifikan faktor musim dalam perilaku penyewaan sepeda.
""")

# 2. Penyewaan Berdasarkan Jam (clean_hour.csv)
st.subheader("Hourly Bike Rentals")

# Load dataset hour
hour_data = pd.read_csv('clean_hour.csv')

# Mengubah kolom date menjadi datetime
hour_data['date'] = pd.to_datetime(hour_data['date'])

# Filter berdasarkan rentang tanggal yang dipilih di sidebar
filtered_hour_data = hour_data[(hour_data['date'] >= pd.to_datetime(start_date)) & 
                               (hour_data['date'] <= pd.to_datetime(end_date))]

# Mengelompokkan dan menghitung total penyewaan berdasarkan jam
hour_rentals = filtered_hour_data.groupby('hr')['total_rentals'].sum()

# Membuat plot batang untuk penyewaan berdasarkan jam
fig, ax = plt.subplots(figsize=(10, 6))
hour_rentals.plot(kind='bar', color='#90CAF9', ax=ax)
ax.set_xlabel("Hour")
ax.set_ylabel("Total Bike Rentals")
ax.set_title("Total Bike Rentals by Hour")
plt.xticks(rotation=90)
st.pyplot(fig)

# Deskripsi gambar
st.markdown("""
**Kesimpulan Grafik Penyewaan Berdasarkan Jam**:  
Jam sibuk, yaitu sekitar jam 8 pagi dan 5 sore, menjadi waktu dengan penyewaan sepeda tertinggi. Ini mengindikasikan penggunaan sepeda terutama sebagai moda transportasi untuk bekerja dan pulang kerja.
""")

# Footer
st.caption('Copyright (C) EKA PUTRA MERAVIGLIOSI 2024')
