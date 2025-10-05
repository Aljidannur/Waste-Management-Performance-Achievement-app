import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu

# Konfigurasi halaman
st.set_page_config(
    page_title="Analisis Pengelolaan Sampah",
    page_icon="♻️",
)

st.title("Analisis Capaian Kinerja Pengelolaan Sampah")
st.markdown("---")

# Load data dari file Excel
path = os.path.dirname(__file__)
my_file = os.path.join(path, '../data/Data Klasterisasi Capaian Kinerja Pengelolaan Sampanh.xlsx')
all_df = pd.read_excel(my_file)

# Sidebar untuk memilih tahun
with st.sidebar:
    selected = option_menu(
        menu_title="Tahun",
        options=sorted(all_df['Tahun'].unique().astype(str)),
        key="pilih_tahun"
    )

# Filter data berdasarkan tahun
df_tahun = all_df[all_df['Tahun'] == int(selected)]

# Menampilkan metrik
col1, col2 = st.columns(2)
with col1:
    rata_kelola = df_tahun["%Sampah Terkelola(B+C)/A"].mean()
    st.metric("Rata-rata Persentase Sampah Terkelola", f"{rata_kelola:.2f}%")

with col2:
    total_timbulan = df_tahun["Timbulan Sampah Tahunan (ton/tahun)(A)"].sum()
    st.metric("Total Timbulan Sampah", f"{total_timbulan:,.0f} ton")

st.markdown("---")


# ===== VISUALISASI: TIMBULAN SAMPAH =====
st.subheader("Timbulan Sampah Tahunan per Kabupaten/Kota")

# Urutkan dari tertinggi ke terendah
df_sorted = df_tahun.sort_values(by="Timbulan Sampah Tahunan (ton/tahun)(A)", ascending=False)

fig_timbulan = px.bar(
    df_sorted,
    x="Kabupaten/Kota",
    y="Timbulan Sampah Tahunan (ton/tahun)(A)",
    text="Timbulan Sampah Tahunan (ton/tahun)(A)",
    color="Timbulan Sampah Tahunan (ton/tahun)(A)",
    color_continuous_scale="Reds",
    labels={"Timbulan Sampah Tahunan (ton/tahun)(A)": "Timbulan Sampah (ton/tahun)", "Kabupaten/Kota": "Wilayah"},
    title=f"Timbulan Sampah Tahunan per Wilayah - Tahun {selected}"
)

fig_timbulan.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
fig_timbulan.update_layout(xaxis_tickangle=-45, height=600)
st.plotly_chart(fig_timbulan, use_container_width=True)

# Interpretasi Timbulan
with st.expander("📝 Interpretasi Timbulan Sampah"):
    wilayah_terbanyak = df_sorted.iloc[0]
    wilayah_tersedikit = df_sorted.iloc[-1]
    st.write(
        f"Pada tahun {selected}, wilayah dengan timbulan sampah **terbanyak** adalah "
        f"**{wilayah_terbanyak['Kabupaten/Kota']}** sebanyak **{wilayah_terbanyak['Timbulan Sampah Tahunan (ton/tahun)(A)']:,.0f} ton**, "
        f"sedangkan yang **paling sedikit** adalah **{wilayah_tersedikit['Kabupaten/Kota']}** dengan hanya "
        f"**{wilayah_tersedikit['Timbulan Sampah Tahunan (ton/tahun)(A)']:,.0f} ton**. "
        f"Tingginya timbulan sampah perlu diimbangi dengan pengelolaan yang optimal agar tidak menimbulkan dampak lingkungan yang besar."
    )
st.markdown("---")
# ===== VISUALISASI 1: GRAFIK BATANG =====
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_tahun["Kabupaten/Kota"],
    y=df_tahun["%Sampah Terkelola(B+C)/A"],
    text=df_tahun["%Sampah Terkelola(B+C)/A"].round(2),
    textposition="auto",
    marker_color='teal'
))
fig.update_layout(
    title=f"Persentase Sampah Terkelola Tiap Kabupaten/Kota - Tahun {selected}",
    xaxis_title="Kabupaten/Kota",
    yaxis_title="% Sampah Terkelola",
    xaxis_tickangle=-45,
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# Interpretasi 1 (EXPANDER)
with st.expander("📝 Interpretasi Grafik Batang"):
    max_row = df_tahun.loc[df_tahun["%Sampah Terkelola(B+C)/A"].idxmax()]
    min_row = df_tahun.loc[df_tahun["%Sampah Terkelola(B+C)/A"].idxmin()]
    st.write(
        f"Pada tahun {selected}, kabupaten/kota dengan persentase pengelolaan sampah tertinggi adalah "
        f"**{max_row['Kabupaten/Kota']}** dengan **{max_row['%Sampah Terkelola(B+C)/A']:.2f}%**, "
        f"sedangkan capaian terendah terdapat di **{min_row['Kabupaten/Kota']}** dengan hanya "
        f"**{min_row['%Sampah Terkelola(B+C)/A']:.2f}%**. Grafik ini membantu mengidentifikasi wilayah yang unggul "
        f"dan yang masih membutuhkan perhatian lebih dalam pengelolaan sampah."
    )
st.markdown("---")
# ===== VISUALISASI: EFISIENSI PENGELOLAAN SAMPAH (RASIO) =====
st.subheader("Efisiensi Pengelolaan Sampah per Wilayah")

# Urutkan dari rasio tertinggi ke terendah
df_rasio = df_tahun.copy()
df_rasio["Rasio Sampah Terkelola"] = df_rasio["%Sampah Terkelola(B+C)/A"] / 100
df_rasio = df_rasio.sort_values(by="Rasio Sampah Terkelola", ascending=False)

fig_rasio = px.bar(
    df_rasio,
    x="Rasio Sampah Terkelola",
    y="Kabupaten/Kota",
    orientation="h",
    color="Rasio Sampah Terkelola",
    color_continuous_scale="Greens",
    labels={"Rasio Sampah Terkelola": "Rasio Sampah Terkelola", "Kabupaten/Kota": "Wilayah"},
    title=f"Efisiensi Pengelolaan Sampah per Wilayah ({selected})",
)

fig_rasio.update_yaxes(categoryorder='total ascending')

fig_rasio.update_layout(height=600)
st.plotly_chart(fig_rasio, use_container_width=True)

# Interpretasi Rasio
with st.expander("📝 Interpretasi Efisiensi Pengelolaan"):
    wilayah_terefisien = df_rasio.iloc[0]
    wilayah_termiskin = df_rasio.iloc[-1]
    st.write(
        f"Efisiensi pengelolaan sampah tertinggi pada tahun {selected} terdapat di **{wilayah_terefisien['Kabupaten/Kota']}** "
        f"dengan rasio **{wilayah_terefisien['Rasio Sampah Terkelola']:.2f}** atau sekitar "
        f"**{wilayah_terefisien['%Sampah Terkelola(B+C)/A']:.2f}%** dari total timbulan. "
        f"Sedangkan wilayah dengan efisiensi terendah adalah **{wilayah_termiskin['Kabupaten/Kota']}** dengan rasio "
        f"**{wilayah_termiskin['Rasio Sampah Terkelola']:.2f}** atau hanya **{wilayah_termiskin['%Sampah Terkelola(B+C)/A']:.2f}%**."
    )
st.markdown("---")
# ===== VISUALISASI 2: SCATTER KASTER =====
st.subheader("Visualisasi Klaster Berdasarkan Prioritas")
fig_kota = px.scatter(
    df_tahun,
    x="%Sampah Terkelola(B+C)/A",
    y="Timbulan Sampah Tahunan (ton/tahun)(A)",
    color="Prioritas",
    text="Kabupaten/Kota",
    color_discrete_map={
        "Prioritas Tinggi": "green",
        "Prioritas Rendah": "red"
    },
    labels={
        "%Sampah Terkelola(B+C)/A": "% Sampah Terkelola",
        "Timbulan Sampah Tahunan (ton/tahun)(A)": "Timbulan Sampah (ton)"
    },
    title=f"Klaster Kabupaten/Kota Berdasarkan Prioritas Pengelolaan Sampah - Tahun {selected}"
)
fig_kota.update_traces(marker=dict(size=12), textposition='top center')
fig_kota.update_layout(height=600)
st.plotly_chart(fig_kota, use_container_width=True)

# Interpretasi 2 (EXPANDER)
with st.expander("📝 Interpretasi Visualisasi Klaster"):
    jumlah_tinggi = df_tahun[df_tahun['Prioritas'] == "Prioritas Tinggi"].shape[0]
    jumlah_rendah = df_tahun[df_tahun['Prioritas'] == "Prioritas Rendah"].shape[0]
    st.write(
        f"Visualisasi scatter plot menggambarkan hubungan antara jumlah timbulan sampah dan persentase pengelolaan sampah. "
        f"Pada tahun {selected}, terdapat **{jumlah_tinggi}** kabupaten/kota dalam kategori **Prioritas Tinggi** "
        f"dan **{jumlah_rendah}** dalam **Prioritas Rendah**. "
        f"Wilayah dalam klaster prioritas tinggi umumnya memiliki nilai pengelolaan yang lebih baik dan perlu dipertahankan, "
        f"sedangkan yang berada pada prioritas rendah memerlukan perhatian dan upaya perbaikan."
    )
st.markdown("---")
# ===== VISUALISASI 3: PIE CHART DISTRIBUSI =====
st.subheader("Distribusi Kabupaten/Kota Berdasarkan Klaster")

# Tambahkan label klaster
df_tahun['Label Klaster'] = df_tahun['Cluster'].map({
    0: "Prioritas Rendah",
    1: "Prioritas Tinggi"
})

# Ringkasan untuk pie chart
cluster_summary = df_tahun.groupby('Label Klaster').agg(
    Jumlah=('Kabupaten/Kota', 'count'),
    Daftar_Kabupaten=('Kabupaten/Kota', lambda x: ', '.join(x))
).reset_index()

# Pie chart
fig_pie = px.pie(
    cluster_summary,
    names='Label Klaster',
    values='Jumlah',
    color='Label Klaster',
    hole=0.4,
    hover_data=['Daftar_Kabupaten'],
    title=f"Distribusi Kabupaten/Kota Berdasarkan Klaster - Tahun {selected}",
    color_discrete_map={
        "Prioritas Tinggi": "lightgreen",
        "Prioritas Rendah": "lightcoral"
    }
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie, use_container_width=True)

# Interpretasi 3 (EXPANDER)
with st.expander("📝 Interpretasi Distribusi Klaster"):
    st.write(
        f"Diagram ini menunjukkan proporsi kabupaten/kota yang termasuk dalam masing-masing klaster prioritas "
        f"pada tahun {selected}. Distribusi ini penting untuk merancang kebijakan yang adil dan berbasis data. "
        f"Wilayah yang masuk dalam klaster **Prioritas Rendah** memerlukan peningkatan kinerja dalam pengelolaan sampah, "
        f"sedangkan **Prioritas Tinggi** dapat dijadikan contoh atau role model untuk wilayah lain."
    )
st.markdown("---")
# ===== OPSIONAL: RINGKASAN AKHIR =====
# with st.expander("📌 Ringkasan Temuan Umum"):
#     st.write(
#         f"Secara keseluruhan, analisis ini bertujuan untuk memberikan wawasan visual mengenai performa pengelolaan sampah "
#         f"tiap daerah di Kalimantan Timur pada tahun {selected}. Hasil ini diharapkan dapat membantu pengambilan keputusan "
#         f"oleh pemangku kebijakan maupun masyarakat untuk mendukung lingkungan yang lebih bersih dan berkelanjutan."
#     )
