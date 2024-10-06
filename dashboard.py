import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur gaya seaborn
sns.set(style="whitegrid")

# Gathering Data
url = 'https://raw.githubusercontent.com/tassyaini/Submission1/refs/heads/main/Data/day.csv'
day_csv = pd.read_csv(url)

# Judul untuk dashboard
st.title('Bike Sharing Data Analysis')

# Displaying the data
st.subheader('Sample of the Data')
st.write(day_csv.head())

# Data Wrangling - Assessing Data
st.subheader('Missing Data Check')
st.write(day_csv.isnull().sum())

# Cleaning Data - Menghapus data yang hilang (jika ada)
day_csv.dropna(axis=0, inplace=True)

# Exploratory Data Analysis (EDA)
st.subheader('Descriptive Statistics')
st.write(day_csv.describe(include="all"))

st.subheader('Aggregate Data by Season')
agg_data = day_csv.groupby(by="season").agg({
    "registered": "nunique",
    "windspeed": ["max", "min", "mean", "std"]
})
st.write(agg_data)

# Visualization 1: Pengaruh musim terhadap jumlah penyewa terdaftar
st.subheader('Pengaruh Musim Terhadap Jumlah Penyewa Terdaftar')

# Membuat plot
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x='season', y='registered', data=day_csv,
            palette={'1': 'lightcoral', '2': 'orange',
                     '3': 'darkorange', '4': 'skyblue'}, ax=ax)

# Menambahkan label dan judul
ax.set_xlabel('Season')
ax.set_ylabel('Registered')
ax.set_title('Pengaruh musim terhadap jumlah penyewa yang terdaftar')
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(['Springer', 'Summer', 'Fall', 'Winter'])

# Menampilkan plot
st.pyplot(fig)

# Visualization 2: Perbandingan pengguna yang terdaftar dan tidak terdaftar (casual) berdasarkan hari dalam minggu
st.subheader('Perbandingan Pengguna Terdaftar dan Tidak Terdaftar per Hari')

# Mengambil data yang diperlukan
days = day_csv['weekday'].tolist()  # Kolom weekday
registered_counts = day_csv['registered'].tolist()  # Kolom registered
casual_counts = day_csv['casual'].tolist()  # Kolom casual

# Membuat DataFrame baru untuk visualisasi
data = {
    'weekday': days,
    'registered': registered_counts,
    'casual': casual_counts
}
df = pd.DataFrame(data)

# Mengubah DataFrame ke format yang panjang (melt)
df_melted = df.melt(id_vars='weekday', value_vars=['registered', 'casual'],
                    var_name='user_type', value_name='count')

# Membuat visualisasi
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(x='weekday', y='count', hue='user_type', data=df_melted,
            hue_order=['registered', 'casual'],  # Mengatur urutan hue
            palette={'registered': 'lightblue', 'casual': 'lightcoral'}, ax=ax2)  # Menentukan warna

# Menambahkan label dan judul
ax2.set_xlabel('Day of the Week (0-6)')
ax2.set_ylabel('Number of Users')
ax2.set_title('Perbandingan Pengguna Terdaftar dan Tidak Terdaftar per Hari')
ax2.set_xticks([0, 1, 2, 3, 4, 5, 6])
ax2.set_xticklabels(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
ax2.legend(title='User Type')

# Menampilkan plot
st.pyplot(fig2)
