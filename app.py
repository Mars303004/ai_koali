import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import time

# ====================
# KONFIGURASI
# ====================
primary_color = "#0057c8"
secondary_color = "#b42020"
bg_color = "#F7FAFC"
font_family = "Arial"

custom_css = f"""
<style>
    /* Base Styling */
    body {{ font-family: {font_family}; }}
    h1 {{ color: {primary_color}; }}
    h2 {{ color: {secondary_color}; }}
    
    /* Navigation Buttons */
    .perspective-btn {{
        background: {primary_color};
        color: white;
        padding: 2rem;
        border-radius: 15px;
        transition: all 0.3s;
        margin: 10px;
        cursor: pointer;
    }}
    .perspective-btn:hover {{
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    
    /* Scorecards */
    .scorecard {{
        background: {bg_color};
        border-radius: 10px;
        padding: 1.5rem;
        margin: 10px 0;
    }}
    
    /* Tabs */
    [data-baseweb="tab-list"] {{
        gap: 10px;
        margin-bottom: 2rem;
    }}
    [data-baseweb="tab"] {{
        padding: 1rem 2rem;
        border-radius: 8px !important;
        background: {bg_color} !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ====================
# KOMPONEN UTAMA
# ====================
def create_gauge(current, previous, title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current,
        delta = {'reference': previous},
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': primary_color},
                 'steps': [{'range': [0, 100], 'color': bg_color}]},
        title = {'text': title}
    ))
    fig.update_layout(height=300, margin=dict(t=50, b=10))
    return fig

def create_scorecard(value, prev_value, title):
    delta = value - prev_value
    return f"""
    <div class="scorecard">
        <div style="font-size:1.2rem; color:#666">{title}</div>
        <div style="font-size:2.5rem; color:{primary_color}">
            {value}% 
            <span style="font-size:1rem; color:{'#2ecc71' if delta >=0 else secondary_color}">
                {"▲" if delta >=0 else "▼"} {abs(delta)}%
            </span>
        </div>
        <div style="color:#999">vs {prev_value}% (Jan)</div>
    </div>
    """

# ====================
# LOGIKA UTAMA
# ====================
def main():
    # Header dan Upload File
    st.title("📊 Performance Dashboard - Februari 2025")
    uploaded_file = st.file_uploader("Upload Data (CSV/Excel)", type=["csv", "xlsx"])
    
    # Filter Bulan
    selected_month = st.selectbox("Pilih Bulan", ["Februari 2025", "Januari 2025"])
    
    # Navigation Buttons
    cols = st.columns(4)
    perspectives = ["Financial", "Customer n Service", "Quality", "Employee"]
    with cols[0]: st.markdown('<div class="perspective-btn" onclick="alert(\'Financial clicked!\')"><h3>💵 Financial</h3></div>', unsafe_allow_html=True)
    with cols[1]: st.markdown('<div class="perspective-btn" onclick="alert(\'Customer clicked!\')"><h3>👥 Customer</h3></div>', unsafe_allow_html=True)
    with cols[2]: st.markdown('<div class="perspective-btn" onclick="alert(\'Quality clicked!\')"><h3>✅ Quality</h3></div>', unsafe_allow_html=True)
    with cols[3]: st.markdown('<div class="perspective-btn" onclick="alert(\'Employee clicked!\')"><h3>👨💼 Employee</h3></div>', unsafe_allow_html=True)

    # Konten Dashboard
    tabs = st.tabs(["Overall BU", "BU1", "BU2", "BU3", "KPI Raw", "SI"])
    
    with tabs[1]:  # BU1
        # Data Sample (Ganti dengan data upload)
        quality_data = {
            "Subdiv 1": {"target": 100, "real": 87, "velocity": 91, "quality": 90},
            "Subdiv 2": {"target": 100, "real": 94, "velocity": 84, "quality": 87},
            "Subdiv 3": {"target": 100, "real": 76, "velocity": 77, "quality": 76}
        }
        
        # Tabs Subdiv/Produk
        subtabs = st.tabs(["Subdiv 1", "Subdiv 2", "Subdiv 3"])
        for idx, tab in enumerate(subtabs):
            with tab:
                data = quality_data[f"Subdiv {idx+1}"]
                
                # Bar Chart
                fig = px.bar(
                    x=["Target", "Realisasi"],
                    y=[data['target'], data['real']],
                    color=[primary_color, secondary_color],
                    labels={"x": "", "y": ""}
                )
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(create_scorecard(data['velocity'], data['velocity']-1, "Velocity"), unsafe_allow_html=True)
                with col2:
                    st.markdown(create_scorecard(data['quality'], data['quality']+1, "Quality"), unsafe_allow_html=True)

    # Tab Lain
    for tab in [tabs[0], tabs[2], tabs[3], tabs[4], tabs[5]]:
        with tab:
            st.warning("⏳ Belum ada data yang tersedia")

    # Export PDF
    if st.button("📤 Export PDF"):
        with st.spinner("Membuat laporan..."):
            time.sleep(2)
            st.success("Laporan berhasil diunduh!")

if __name__ == "__main__":
    main()
