import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import os
import base64
import pandas as pd  

# Konfigurasi halaman
st.set_page_config(
    page_title="Capaian Kinerja Pengelolaan Sampah Provinsi Kalimantan Timur",
    page_icon="📊",
)


st.markdown("""
    <h1 style='text-align: center;'>
        Dashboard Capaian Kinerja Pengelolaan Sampah Provinsi Kalimantan Timur
    </h1>
           
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="DASHBOARD",
        options=["Proyek", "Tentang Dataset"],
    )

# Fungsi bantu untuk encode gambar
def image_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Halaman "About Projects"
if selected == "Proyek":
    path = os.path.dirname(__file__)
    my_file = os.path.join(path, 'images/img4.jpg')  
    if os.path.exists(my_file):
        img_base64 = image_to_base64(my_file)

        st.markdown(
            f"""
            <div style='text-align: center;'>
                <img src="data:image/jpeg;base64,{img_base64}" width="650">
            </div>
            """,
            unsafe_allow_html=True
        )

        # Interpretasi singkat
        st.markdown("""
        <div style='text-align: justify; margin-top: 10px;'>
           
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Gambar tidak ditemukan di folder `images/`.")

# Halaman "Dataset Overview"
if selected == "Tentang Dataset":
    path = os.path.dirname(__file__)
    my_file = os.path.join(path, 'data/Data 6 Tahun.csv.xlsx') 

    if os.path.exists(my_file):
        all_df = pd.read_excel(my_file)

        st.subheader("Dataset Capaian Kinerja Pengelolaan Sampah Provinsi Kalimantan")
        st.dataframe(all_df)

        st.subheader("Tentang Dataset")

        st.markdown("""
       Dataset yang digunakan dalam dashboard ini merupakan data capaian kinerja pengelolaan sampah dari seluruh kabupaten/kota di Provinsi Kalimantan Timur, yang diperoleh dari Sistem Informasi Pengelolaan Sampah Nasional (SIPSN)
        """, unsafe_allow_html=True)


       