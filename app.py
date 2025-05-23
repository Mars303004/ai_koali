import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Konfigurasi warna
primary_color = "#0057c8"
secondary_color = "#b42020"
bg_color = "#F7FAFC"

st.set_page_config(layout="wide")

# Fungsi untuk tampilan Quality Perspective
def show_quality(data, month):
    st.subheader("Quality Performance")
    subdivs = st.tabs(["Subdiv 1", "Subdiv 2", "Subdiv 3"])
    
    with subdivs[0]:  # Subdiv 1
        col1, col2 = st.columns(2)
        with col1:
            # Bar Chart Target vs Realisasi
            fig = px.bar(data, x='Metric', y='Value', color='Metric',
                        color_discrete_map={'Target': primary_color, 'Realisasi': secondary_color})
            fig.update_layout(title="Target vs Realisasi", height=300)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Gauge Velocity
            velocity = 95  # Contoh data
            prev_velocity = 90  # Data Januari
            arrow = "↑" if velocity >= prev_velocity else "↓"
            color = "green" if velocity >= prev_velocity else "red"
            
            st.markdown(f"""
            <div style="background-color:{bg_color}; padding:20px; border-radius:10px; text-align:center">
                <h3 style="color:{primary_color}">Velocity</h3>
                <h1 style="color:{color}; font-size:50px; margin:0">{velocity}% 
                    <span style="font-size:30px; color:{color}">{arrow}</span>
                </h1>
                <p>vs {prev_velocity}% (Januari)</p>
            </div>
            """, unsafe_allow_html=True)

# Layout Utama
def main():
    st.title("🚀 BU1 Performance Dashboard - Februari 2025")
    
    # Header dengan tombol
    with st.container():
        cols = st.columns(4)
        perspectives = ["Financial", "Customer", "Quality", "Employee"]
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div style='background-color:{primary_color};color:white;padding:20px;border-radius:10px;text-align:center'><h2>{perspectives[i]}</h2></div>", 
                          unsafe_allow_html=True)
    
    # Filter Bulan
    selected_month = st.selectbox("Pilih Bulan", ["Februari 2025", "Januari 2025"])
    
    # Contoh Data Quality
    quality_data = pd.DataFrame({
        'Metric': ['Target', 'Realisasi'],
        'Value': [100, 95]
    })
    
    # Tab Utama
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overall BU", "BU1", "BU2", "BU3", "KPI Raw", "SI"])
    
    with tab2:  # BU1
        show_quality(quality_data, selected_month)
        
    # Fitur Upload & Export
    with st.sidebar:
        st.header("📤 Upload Data")
        uploaded_file = st.file_uploader("Unggah file CSV/Excel")
        
        if st.button("Export ke PDF"):
            # Implementasi export PDF disini
            pdf_buffer = BytesIO()
            st.success("PDF berhasil di-generate!")
    
    # Pesan untuk tab kosong
    for tab in [tab1, tab3, tab4, tab5, tab6]:
        with tab:
            st.warning("Belum ada data yang tersedia")

if __name__ == "__main__":
    main()
