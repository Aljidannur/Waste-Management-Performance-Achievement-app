import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Mapping",
    page_icon="🗺️",
)

st.title("🗺️ Mapping Klaster Pengelolaan Sampah")

# Koordinat kabupaten/kota
koordinat_kota = {
    "Kab. Paser": [-1.9981, 116.4378],
    "Kab. Kutai Kartanegara": [-0.4043, 116.9858],
    "Kab. Berau": [2.1617, 117.4006],
    "Kab. Kutai Barat": [0.1467, 115.6789],
    "Kab. Kutai Timur": [0.4461, 117.5898],
    "Kab. Penajam Paser Utara": [-1.2913, 116.5693],
    "Kab. Mahakam Ulu": [0.9023, 114.8000],
    "Kota Balikpapan": [-1.2692, 116.8253],
    "Kota Samarinda": [-0.5022, 117.1537],
    "Kota Bontang": [0.1333, 117.5],
}

# Load data Excel
path = os.path.dirname(__file__)
data_path = os.path.join(path, '../data/Data Klasterisasi Capaian Kinerja Pengelolaan Sampanh.xlsx')
df = pd.read_excel(data_path)

# Tambahkan koordinat
df["Latitude"] = df["Kabupaten/Kota"].map(lambda x: koordinat_kota.get(x.strip(), [None, None])[0])
df["Longitude"] = df["Kabupaten/Kota"].map(lambda x: koordinat_kota.get(x.strip(), [None, None])[1])

# Mapping cluster ke label
cluster_map = {
    0: "Prioritas Tinggi",
    1: "Prioritas Rendah"
}
color_map = {
    "Prioritas Tinggi": "red",
    "Prioritas Rendah": "green"
}
df["Prioritas"] = df["Cluster"].map(cluster_map)

# Sidebar filter
with st.sidebar:
    st.header("📍 Filter Peta")
    selected_year = st.radio("Pilih Tahun", sorted(df["Tahun"].unique()))
    selected_prioritas = st.multiselect(
        "Pilih Kategori Prioritas",
        options=df["Prioritas"].unique(),
        default=df["Prioritas"].unique()
    )

# Filter berdasarkan tahun dan prioritas
df_filtered = df[df["Tahun"] == selected_year]
if selected_prioritas:
    df_filtered = df_filtered[df_filtered["Prioritas"].isin(selected_prioritas)]

# Buat peta fokus Kalimantan Timur
# Koordinat tengah Kalimantan Timur: lat 0.5, lon 117.0
m = folium.Map(location=[0.5, 117.0], zoom_start=7,
               max_bounds=True,
               min_zoom=6,
               max_zoom=10)

# Tambahkan titik lokasi
for _, row in df_filtered.iterrows():
    if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
        warna = color_map.get(row["Prioritas"], "blue")
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=8,
            color=warna,
            fill=True,
            fill_color=warna,
            fill_opacity=0.7,
            popup=folium.Popup(
                f"{row['Kabupaten/Kota']}<br>{row['Prioritas']}",
                max_width=300
            )
        ).add_to(m)

# Tampilkan peta ke aplikasi
st_folium(m, width=800, height=550)

# Interpretasi klaster tahunan
with st.expander("ℹ️ Interpretasi Klaster Berdasarkan Tahun"):
    total_daerah = len(df_filtered)
    tinggi = df_filtered[df_filtered["Prioritas"] == "Prioritas Tinggi"]
    rendah = df_filtered[df_filtered["Prioritas"] == "Prioritas Rendah"]

    tinggi_list = ", ".join(sorted(tinggi["Kabupaten/Kota"].tolist()))
    rendah_list = ", ".join(sorted(rendah["Kabupaten/Kota"].tolist()))

    st.markdown(f"""
    Pada tahun **{selected_year}**, hasil klasterisasi menunjukkan bahwa dari total **{total_daerah} kabupaten/kota** di Provinsi Kalimantan Timur:

    - 🟥 **{len(tinggi)} wilayah** termasuk dalam **Prioritas Tinggi**, yaitu:
      _{tinggi_list}_.

    - 🟩 **{len(rendah)} wilayah** termasuk dalam **Prioritas Rendah**, yaitu:
      _{rendah_list}_.

    Klasifikasi ini membantu mengidentifikasi daerah yang membutuhkan perhatian lebih besar dalam pengelolaan sampah dan dapat menjadi dasar penentuan kebijakan intervensi.
    """)

