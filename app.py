import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
import time

# ====================
# STYLING & THEMING
# ====================
primary_color = "#0057c8"
secondary_color = "#b42020"
bg_color = "#F7FAFC"
font_family = "Arial"

custom_css = f"""
<style>
    /* Typography */
    h1 {{ font-family: {font_family}; color: {primary_color}!important; }}
    h2 {{ font-family: {font_family}; color: {secondary_color}!important; }}
    .metric-label {{ font-size: 1.2rem!important; color: #555; }}
    
    /* Scorecards */
    .scorecard {{
        background: {bg_color};
        border-radius: 10px;
        padding: 20px;
        transition: transform 0.3s ease;
    }}
    .scorecard:hover {{ transform: translateY(-5px); }}
    
    /* Filters */
    .stSelectbox > div {{ 
        border: 2px solid {primary_color}!important;
        border-radius: 8px;
        padding: 5px;
    }}
    
    /* Loading Animation */
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    .spinner {{
        animation: spin 1s linear infinite;
        border: 4px solid {primary_color};
        border-radius: 50%;
        border-top-color: transparent;
        width: 40px;
        height: 40px;
        margin: 20px auto;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ====================
# CUSTOM COMPONENTS
# ====================
def create_gauge(value, prev_value, title):
    delta = value - prev_value
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        delta = {'reference': prev_value},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': primary_color},
            'steps' : [{'range': [0, 100], 'color': bg_color}]
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=50, b=10),
        font={'family': font_family}
    )
    return fig

def create_scorecard(title, value, comparison_value):
    delta = value - comparison_value
    arrow = "▲" if delta >=0 else "▼"
    color = "#2ECC71" if delta >=0 else secondary_color
    return f"""
    <div class="scorecard">
        <div class="metric-label">{title}</div>
        <div style="font-size: 2.5rem; color: {primary_color}; margin: 10px 0">
            {value}%
            <span style="font-size: 1.2rem; color: {color}">{arrow} {abs(delta)}%</span>
        </div>
        <div style="color: #666">vs {comparison_value}% (Jan)</div>
    </div>
    """

# ====================
# DATA HANDLING
# ====================
@st.cache_data
def load_sample_data():
    return pd.DataFrame({
        'Month': ['Jan-25', 'Feb-25']*3,
        'Subdiv': ['Subdiv 1', 'Subdiv 1', 'Subdiv 2', 'Subdiv 2', 'Subdiv 3', 'Subdiv 3'],
        'Target': [100]*6,
        'Realisasi': [85, 87, 86, 94, 77, 76],
        'Velocity': [90, 91, 85, 84, 76, 77],
        'Quality': [91, 90, 95, 94, 90, 89]
    })

# ====================
# MAIN LAYOUT
# ====================
def main():
    st.title("📊 BU1 Performance Dashboard")
    
    # Header with Perspective Navigation
    cols = st.columns([2,1,2,1])
    perspectives = ["Financial", "Customer", "Quality", "Employee"]
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; 
                        background: {primary_color}; color: white; 
                        border-radius: 10px; margin: 5px; 
                        cursor: pointer">
                {perspectives[i]}
            </div>
            """, unsafe_allow_html=True)
    
    # Main Content Area
    with st.container():
        # Filters Row
        col1, col2 = st.columns([3,1])
        with col1:
            selected_month = st.selectbox("Month", ["Feb-25", "Jan-25"])
        with col2:
            refresh_btn = st.button("🔄 Refresh Data", type="secondary")
        
        # Quality Perspective
        st.subheader(f"Quality Performance - {selected_month}")
        
        # Data Loading State
        if refresh_btn:
            with st.spinner():
                with st.empty():
                    st.markdown("<div class='spinner'></div>", unsafe_allow_html=True)
                    time.sleep(2)  # Simulate API call
                
        # Load Data
        df = load_sample_data()
        
        # Tabs for Subdivisions
        tab1, tab2, tab3 = st.tabs(["Subdiv 1", "Subdiv 2", "Subdiv 3"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(
                    df[df['Subdiv'] == 'Subdiv 1'],
                    x='Month',
                    y=['Target', 'Realisasi'],
                    barmode='group',
                    color_discrete_sequence=[primary_color, secondary_color]
                )
                fig.update_layout(title="Target vs Realisasi", height=400)
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.markdown(create_scorecard("Velocity", 91, 90), unsafe_allow_html=True)
                st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                st.markdown(create_scorecard("Quality", 90, 91), unsafe_allow_html=True)

        # Drill-Down Modal
        if st.session_state.get('show_modal'):
            with st.columns([1,6,1])[1]:
                st.markdown("""
                <div style="background: white; padding: 20px; border-radius: 10px; 
                            box-shadow: 0 0 20px rgba(0,0,0,0.1); margin-top: 20px">
                    <h3>Detail Analysis</h3>
                    <p>Detailed metrics would appear here...</p>
                    <button onclick="window.parent.document.querySelector('.stButton button').click()" 
                            style="background: #0057c8; color: white; border: none; 
                                   padding: 8px 16px; border-radius: 5px">
                        Close
                    </button>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
