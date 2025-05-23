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

st.set_page_config(layout="wide")

# ====================
# KOMPONEN KUSTOM
# ====================
def create_gauge(current, previous, title):
    delta_value = current - previous
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current,
        delta = {
            'reference': previous,
            'increasing': {'color': '#2ecc71'}, 
            'decreasing': {'color': secondary_color}
        },
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': primary_color},
            'steps': [{'range': [0, 100], 'color': bg_color}]
        },
        number = {'font': {'color': '#2ecc71' if delta_value >=0 else secondary_color}},
    ))
    fig.update_layout(
        height=300,
        margin=dict(t=50, b=10),
        font={'family': font_family}
    )
    return fig

def create_scorecard(value, prev_value, title):
    delta = value - prev_value
    return f"""
    <div style="background:{bg_color}; border-radius:10px; padding:20px; margin:10px">
        <div style="font-size:1.2rem; color:#666">{title}</div>
        <div style="font-size:2.5rem; color:{primary_color}">
            {value}
            <span style="font-size:1rem; color:{'#2ecc71' if delta >=0 else secondary_color}">
                {'▲' if delta >=0 else '▼'} {abs(delta)}
            </span>
        </div>
        <div style="color:#999">vs {prev_value} (Jan)</div>
    </div>
    """

# ====================
# DATA & LAYOUT
# ====================
def financial_perspective():
    st.header("Financial Performance")
    
    # Data Contoh
    data = {
        "Budget": 1_500_000,
        "Expense": 1_200_000,
        "Usage": 80,
        "Profit": 250_000,
        "Revenue": 1_750_000
    }
    prev_data = {
        "Budget": 1_400_000,
        "Expense": 1_300_000,
        "Usage": 75,
        "Profit": 200_000,
        "Revenue": 1_600_000
    }
    
    # Bar Chart + Gauge
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            x=["Budget", "Expense"],
            y=[data["Budget"], data["Expense"]],
            color=[primary_color, secondary_color],
            labels={"x": "", "y": "Amount"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.plotly_chart(create_gauge(data["Usage"], prev_data["Usage"], "Usage"), use_container_width=True)
    
    # Scorecards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(create_scorecard(data["Profit"], prev_data["Profit"], "Profit"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_scorecard(data["Revenue"], prev_data["Revenue"], "Revenue"), unsafe_allow_html=True)

def customer_perspective():
    st.header("Customer Service Performance")
    
    # Data Contoh
    data = {
        "Customers": 150,
        "Satisfaction": 4.5
    }
    prev_data = {
        "Customers": 120,
        "Satisfaction": 4.3
    }
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            names=["Current Customers", "New Customers"],
            values=[data["Customers"], 30],
            hole=0.6,
            color_discrete_sequence=[primary_color, secondary_color]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.plotly_chart(create_gauge(data["Satisfaction"]*20, prev_data["Satisfaction"]*20, "Satisfaction"), 
                      use_container_width=True)

def quality_perspective():
    st.header("Quality Performance")
    
    # Data Contoh
    data = {
        "Target": 100,
        "Realisasi": 87,
        "Velocity": 91,
        "Quality": 90
    }
    prev_data = {
        "Target": 100,
        "Realisasi": 85,
        "Velocity": 90,
        "Quality": 91
    }
    
    # Bar Chart
    fig = px.bar(
        x=["Target", "Realisasi"],
        y=[data["Target"], data["Realisasi"]],
        color=[primary_color, secondary_color],
        labels={"x": "", "y": "Value"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Scorecards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(create_scorecard(data["Velocity"], prev_data["Velocity"], "Velocity"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_scorecard(data["Quality"], prev_data["Quality"], "Quality"), unsafe_allow_html=True)

def employee_perspective():
    st.header("Employee Performance")
    
    # Data Contoh
    data = {
        "Current MP": 85,
        "Needed MP": 100,
        "Competency": 4.2,
        "Turnover": 8.5
    }
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            names=["Current MP", "Required"],
            values=[data["Current MP"], data["Needed MP"] - data["Current MP"]],
            hole=0.6,
            color_discrete_sequence=[primary_color, secondary_color]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(create_scorecard(data["Competency"], 4.0, "Competency"), unsafe_allow_html=True)
        st.markdown(create_scorecard(data["Turnover"], 9.2, "Turnover Ratio"), unsafe_allow_html=True)

# ====================
# MAIN LAYOUT
# ====================
def main():
    st.title("🚀 Dynamic Performance Dashboard")
    
    # Upload File
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
    
    # Filter Bulan
    selected_month = st.selectbox("Pilih Bulan", ["Februari 2025", "Januari 2025"])
    
    # Navigation Buttons
    perspectives = ["Financial", "Customer n Service", "Quality", "Employee"]
    cols = st.columns(4)
    for idx, perspective in enumerate(perspectives):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align:center; background:{primary_color}; color:white; 
                        padding:30px; border-radius:15px; margin:10px; cursor:pointer"
                onclick="alert('{perspective} clicked!')">
                <h3>{perspective}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabs Dinamis
    tabs = st.tabs(["Subdiv 1", "Subdiv 2", "Subdiv 3"]) if st.session_state.get("perspective") != "Customer" else st.tabs(["PRODUK 1", "PRODUK 2", "PRODUK 3"])
    
    # Contoh Implementasi Financial
    financial_perspective()

if __name__ == "__main__":
    main()
