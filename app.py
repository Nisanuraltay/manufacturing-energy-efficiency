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


# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "🔧 Machine Analysis", 
    "🗄️ SQL Queries", 
    "🤖 ML Model"
])



# ═══════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════════════
with tab1:
    
    # ROW 1: RPM Distribution + Failure Pie
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### RPM Distribution — Normal vs High-Risk")
        st.caption("IQR method · Threshold: 1139–1895 RPM")
        
        # Create bins for RPM
        bins = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 2000, 2500, 3000]
        df['rpm_bin'] = pd.cut(df['Rotational speed [rpm]'], bins=bins)
        
        normal_rpm = df[df['high_risk_rpm']==0]['rpm_bin'].value_counts().sort_index()
        highrisk_rpm = df[df['high_risk_rpm']==1]['rpm_bin'].value_counts().sort_index()
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            name='Normal (9,582)',
            x=[str(x) for x in normal_rpm.index],
            y=normal_rpm.values,
            marker_color='rgba(56,189,248,0.15)',
            marker_line_color='rgba(56,189,248,1)',
            marker_line_width=1.5
        ))
        fig1.add_trace(go.Bar(
            name='High-Risk (418)',
            x=[str(x) for x in highrisk_rpm.index],
            y=highrisk_rpm.values,
            marker_color='rgba(248,113,113,0.15)',
            marker_line_color='rgba(248,113,113,1)',
            marker_line_width=1.5
        ))
        fig1.update_layout(
            barmode='group',
            height=350,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#4a6072', size=10),
            xaxis=dict(gridcolor='#1e2738', title='RPM Range'),
            yaxis=dict(gridcolor='#1e2738', title='Machine Count'),
            legend=dict(orientation='h', y=-0.15),
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Failure Type Distribution")
        st.caption("348 total failure records")
        
        failure_counts = df['Failure Type'].value_counts()
        
        fig2 = go.Figure(data=[go.Pie(
            labels=failure_counts.index,
            values=failure_counts.values,
            hole=0.6,
            marker=dict(
                colors=['rgba(74,222,128,0.2)', 'rgba(251,146,60,1)', 
                       'rgba(248,113,113,1)', 'rgba(251,191,36,1)', 
                       'rgba(167,139,250,1)', 'rgba(56,189,248,1)'],
                line=dict(color='#07090f', width=3)
            ),
            textposition='inside',
            textinfo='percent+label',
            textfont=dict(size=9)
        )])
        fig2.update_layout(
            height=350,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=9),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 2: Type + Efficiency + Priority
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Machine Type Distribution")
        st.caption("L / M / H type fleet")
        
        type_counts = df.groupby(['Type', 'high_risk_rpm']).size().unstack(fill_value=0)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name='Normal',
            x=['L-Type', 'M-Type', 'H-Type'],
            y=type_counts[0].values,
            marker_color='rgba(56,189,248,0.15)',
            marker_line_color='rgba(56,189,248,1)',
            marker_line_width=1.5
        ))
        fig3.add_trace(go.Bar(
            name='High-Risk',
            x=['L-Type', 'M-Type', 'H-Type'],
            y=type_counts[1].values,
            marker_color='rgba(248,113,113,0.15)',
            marker_line_color='rgba(248,113,113,1)',
            marker_line_width=1.5
        ))
        fig3.update_layout(
            barmode='stack',
            height=280,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#4a6072', size=10),
            xaxis=dict(gridcolor='#1e2738'),
            yaxis=dict(gridcolor='#1e2738'),
            legend=dict(orientation='h', y=-0.2),
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("#### Normal vs High-Risk Efficiency")
        st.caption("Efficiency Score comparison")
        
        normal_eff = df[df['high_risk_rpm']==0]['efficiency_score'].mean()
        highrisk_eff = df[df['high_risk_rpm']==1]['efficiency_score'].mean()
        
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=['Normal Machines', 'High-Risk Machines'],
            y=[normal_eff, highrisk_eff],
            marker=dict(
                color=['rgba(74,222,128,0.15)', 'rgba(248,113,113,0.15)'],
                line=dict(color=['rgba(74,222,128,1)', 'rgba(248,113,113,1)'], width=2)
            ),
            text=[f'{normal_eff:.2f}', f'{highrisk_eff:.2f}'],
            textposition='outside'
        ))
        fig4.update_layout(
            height=280,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#4a6072', size=10),
            xaxis=dict(gridcolor='#1e2738'),
            yaxis=dict(gridcolor='#1e2738', range=[20, 45]),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with col3:
        st.markdown("#### Optimization Priority Distribution")
        st.caption("Score 0–5 · 418 critical machines (4-5)")
        
        priority_counts = df['optimization_priority'].value_counts().sort_index()
        
        colors = ['rgba(74,222,128,0.15)', 'rgba(74,222,128,0.15)', 
                 'rgba(251,191,36,0.15)', 'rgba(251,191,36,0.15)',
                 'rgba(248,113,113,0.15)', 'rgba(248,113,113,0.15)']
        borders = ['rgba(74,222,128,1)', 'rgba(74,222,128,1)', 
                  'rgba(251,191,36,1)', 'rgba(251,191,36,1)',
                  'rgba(248,113,113,1)', 'rgba(248,113,113,1)']
        
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=priority_counts.index,
            y=priority_counts.values,
            marker=dict(color=colors, line=dict(color=borders, width=1.5))
        ))
        fig5.update_layout(
            height=280,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#4a6072', size=10),
            xaxis=dict(gridcolor='#1e2738', title='Priority Score'),
            yaxis=dict(gridcolor='#1e2738', title='Machine Count'),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        st.caption("🟢 0-1: Normal | 🟡 2-3: Monitor | 🔴 4-5: URGENT")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 3: Correlation Scatter
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### RPM — Efficiency Correlation")
        st.caption("High RPM = Low Efficiency")
        
        fig6 = go.Figure()
        
        normal_data = df[df['high_risk_rpm']==0].sample(min(500, len(df[df['high_risk_rpm']==0])))
        highrisk_data = df[df['high_risk_rpm']==1]
        
        fig6.add_trace(go.Scatter(
            x=normal_data['Rotational speed [rpm]'],
            y=normal_data['efficiency_score'],
            mode='markers',
            name='Normal',
            marker=dict(color='rgba(56,189,248,0.6)', size=4)
        ))
        fig6.add_trace(go.Scatter(
            x=highrisk_data['Rotational speed [rpm]'],
            y=highrisk_data['efficiency_score'],
            mode='markers',
            name='High-Risk',
            marker=dict(color='rgba(248,113,113,0.8)', size=5)
        ))
        fig6.update_layout(
            height=300,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#4a6072', size=10),
            xaxis=dict(gridcolor='#1e2738', title='RPM'),
            yaxis=dict(gridcolor='#1e2738', title='Efficiency Score'),
            legend=dict(orientation='h', y=-0.2),
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        st.markdown("#### Temperature Profile (Air vs Process)")
        st.caption("Kelvin distribution")
        
        sample_data = df.sample(min(500, len(df)))
        
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(
            x=sample_data['Air temperature [K]'],
            y=sample_data['Process temperature [K]'],
            mode='markers',
            marker=dict(color='rgba(251,146,60,0.6)', size=3),
            name='Temperature'
        ))
        fig7.update_layout(
            height=300,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#4a6072', size=10),
            xaxis=dict(gridcolor='#1e2738', title='Air Temperature (K)'),
            yaxis=dict(gridcolor='#1e2738', title='Process Temperature (K)'),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=40)
        )
        st.plotly_chart(fig7, use_container_width=True)


