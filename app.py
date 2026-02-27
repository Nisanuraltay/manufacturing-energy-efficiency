import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config - EN BAŞTA OLMALI!
st.set_page_config(
    page_title="⚡ Energy Efficiency Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #07090f;
        color: #cdd9e5;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #0d1117 0%, #161b24 100%);
        border: 1px solid #1e2738;
        border-radius: 12px;
        padding: 20px 30px;
        margin-bottom: 24px;
    }
    
    /* KPI cards */
    .stMetric {
        background: #0d1117;
        border: 1px solid #1e2738;
        border-radius: 10px;
        padding: 16px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #0d1117;
        border: 1px solid #1e2738;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 20px;
        font-size: 13px;
        font-weight: 600;
        color: #4a6072;
    }
    
    .stTabs [aria-selected="true"] {
        background: #161b24;
        color: #cdd9e5;
    }
    
    /* Cards */
    div[data-testid="stExpander"] {
        background: #0d1117;
        border: 1px solid #1e2738;
        border-radius: 10px;
    }
    
    /* Hide default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load REAL data
@st.cache_data
def load_data():
    # BURAYA SENİN CSV YOLUNU KOY
    # GitHub'daysa: 
    df = pd.read_csv('https://raw.githubusercontent.com/Nisanuraltay/manufacturing-energy-efficiency/main/data/predictive_maintenance.csv')
    
    # Data preparation (Notebook 2'den)
    df['Rotational speed [rpm]'] = df['Rotational speed [rpm]'].astype(float)
    df['Torque [Nm]'] = df['Torque [Nm]'].astype(float)
    df['Tool wear [min]'] = df['Tool wear [min]'].astype(float)
    df['Target'] = df['Target'].astype(float)
    
    # Temperature
    df['temp_difference'] = df['Process temperature [K]'] - df['Air temperature [K]']
    
    # High-risk label
    rpm = df['Rotational speed [rpm]']
    Q1, Q3 = rpm.quantile(0.25), rpm.quantile(0.75)
    IQR = Q3 - Q1
    df['high_risk_rpm'] = ((rpm < Q1 - 1.5*IQR) | (rpm > Q3 + 1.5*IQR)).astype(int)
    
    # Metrics
    df['power_consumption_kw'] = ((df['Rotational speed [rpm]'] / 1000) * 
                                   (df['Torque [Nm]'] / 100) * 1.73)
    df['efficiency_score'] = df['Torque [Nm]'] / df['power_consumption_kw']
    df['cost_per_hour_tl'] = df['power_consumption_kw'] * 1.2
    
    # Priority
    def calc_priority(row):
        score = 0
        if row['high_risk_rpm'] == 1: score += 2
        if row['efficiency_score'] < df['efficiency_score'].median(): score += 2
        if row['Target'] == 1: score += 1
        return min(score, 5)
    
    df['optimization_priority'] = df.apply(calc_priority, axis=1)
    
    return df

df = load_data()

# HEADER
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #38bdf8, #4ade80); 
                        border-radius: 12px; display: flex; align-items: center; justify-content: center; 
                        font-size: 28px; box-shadow: 0 0 20px rgba(56,189,248,0.3);">
                ⚡
            </div>
            <div>
                <h1 style="margin: 0; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">
                    Manufacturing Energy Efficiency Analysis
                </h1>
                <p style="margin: 4px 0 0; font-size: 11px; color: #4a6072; letter-spacing: 1.5px; text-transform: uppercase;">
                    Predictive Maintenance · 10,000 Machines · N.Nur Altay
                </p>
            </div>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
            <div style="padding: 8px 16px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); 
                        border-radius: 20px; font-size: 11px; color: #4ade80; display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background: #4ade80; border-radius: 50%; animation: pulse 2s infinite;"></div>
                Live Dashboard
            </div>
            <div style="padding: 8px 16px; background: #161b24; border: 1px solid #1e2738; 
                        border-radius: 20px; font-size: 11px; color: #4a6072;">
                Feb 2026
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# KPI METRICS
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🏭 Total Machines",
        value=f"{len(df):,}",
        delta="3 Types (L/M/H)"
    )

with col2:
    high_risk_count = df['high_risk_rpm'].sum()
    st.metric(
        label="⚠️ High-Risk",
        value=f"{high_risk_count}",
        delta=f"{high_risk_count/len(df)*100:.2f}%",
        delta_color="inverse"
    )

with col3:
    normal_eff = df[df['high_risk_rpm']==0]['efficiency_score'].mean()
    st.metric(
        label="📈 Avg Efficiency (Normal)",
        value=f"{normal_eff:.2f}",
        delta="+27.8% vs High-Risk"
    )

with col4:
    avg_cost = df['cost_per_hour_tl'].mean()
    st.metric(
        label="💰 Avg Hourly Cost",
        value=f"{avg_cost:.2f} TL/hr",
        delta="1.2 TL/kWh"
    )

with col5:
    failure_count = int(df['Target'].sum())
    st.metric(
        label="🔥 Failure Records",
        value=f"{failure_count}",
        delta=f"{failure_count/len(df)*100:.2f}%",
        delta_color="inverse"
    )

st.markdown("<br>", unsafe_allow_html=True)

# INSIGHT
st.info("""
💡 **Key Finding:** 418 high-risk machines have **27.8% lower efficiency** compared to normal machines 
(27.76 vs 38.45). These machines operate with **high RPM + low torque**, wasting energy. 
Annual cost impact: **~2.96M TL**.
""")



