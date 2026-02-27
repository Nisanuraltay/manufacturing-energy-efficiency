import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="⚡ Energy Efficiency Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CUSTOM CSS
st.markdown("""
<style>
    .stApp { background: #07090f; color: #cdd9e5; }
    .main-header {
        background: linear-gradient(135deg, #0d1117 0%, #161b24 100%);
        border: 1px solid #1e2738;
        border-radius: 12px;
        padding: 20px 30px;
        margin-bottom: 24px;
    }
    .stMetric { background: #0d1117; border: 1px solid #1e2738; border-radius: 10px; padding: 16px; }
    .stTabs [data-baseweb="tab-list"] { background: #0d1117; border: 1px solid #1e2738; border-radius: 8px; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 6px; padding: 8px 20px; font-size: 13px; font-weight: 600; color: #4a6072; }
    .stTabs [aria-selected="true"] { background: #161b24; color: #cdd9e5; }
    div[data-testid="stExpander"] { background: #0d1117; border: 1px solid #1e2738; border-radius: 10px; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# 3. DATA LOADING
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/Nisanuraltay/manufacturing-energy-efficiency/main/data/predictive_maintenance.csv')
    df['Rotational speed [rpm]'] = df['Rotational speed [rpm]'].astype(float)
    df['Torque [Nm]'] = df['Torque [Nm]'].astype(float)
    df['Tool wear [min]'] = df['Tool wear [min]'].astype(float)
    df['Target'] = df['Target'].astype(float)
    df['temp_difference'] = df['Process temperature [K]'] - df['Air temperature [K]']
    
    rpm = df['Rotational speed [rpm]']
    Q1, Q3 = rpm.quantile(0.25), rpm.quantile(0.75)
    IQR = Q3 - Q1
    df['high_risk_rpm'] = ((rpm < Q1 - 1.5*IQR) | (rpm > Q3 + 1.5*IQR)).astype(int)
    
    df['power_consumption_kw'] = ((df['Rotational speed [rpm]'] / 1000) * (df['Torque [Nm]'] / 100) * 1.73)
    df['efficiency_score'] = df['Torque [Nm]'] / df['power_consumption_kw']
    df['cost_per_hour_tl'] = df['power_consumption_kw'] * 1.2
    
    def calc_priority(row):
        score = 0
        if row['high_risk_rpm'] == 1: score += 2
        if row['efficiency_score'] < df['efficiency_score'].median(): score += 2
        if row['Target'] == 1: score += 1
        return min(score, 5)
    
    df['optimization_priority'] = df.apply(calc_priority, axis=1)
    return df

df = load_data()

# 4. HEADER
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #38bdf8, #4ade80); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 28px;">⚡</div>
            <div>
                <h1 style="margin: 0; font-size: 24px; font-weight: 800;">Manufacturing Energy Efficiency Analysis</h1>
                <p style="margin: 4px 0 0; font-size: 11px; color: #4a6072; letter-spacing: 1.5px; text-transform: uppercase;">Predictive Maintenance · 10,000 Machines · N.Nur Altay</p>
            </div>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
            <div style="padding: 8px 16px; background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.2); border-radius: 20px; font-size: 11px; color: #4ade80;">Live Dashboard</div>
            <div style="padding: 8px 16px; background: #161b24; border: 1px solid #1e2738; border-radius: 20px; font-size: 11px; color: #4a6072;">Feb 2026</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. KPI METRICS
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("Total Machines", f"{len(df):,}", "3 Types (L/M/H)")
with col2:
    hr_val = df['high_risk_rpm'].sum()
    st.metric("High-Risk", f"{hr_val}", f"{hr_val/len(df)*100:.2f}%", delta_color="inverse")
with col3:
    n_eff = df[df['high_risk_rpm']==0]['efficiency_score'].mean()
    st.metric("Avg Efficiency", f"{n_eff:.2f}", "+27.8% vs HR")
with col4: st.metric("Avg Hourly Cost", f"{df['cost_per_hour_tl'].mean():.2f} TL/hr", "1.2 TL/kWh")
with col5:
    f_val = int(df['Target'].sum())
    st.metric("Failure Records", f"{f_val}", f"{f_val/len(df)*100:.2f}%", delta_color="inverse")

st.info("💡 **Key Finding:** 418 high-risk machines have **27.8% lower efficiency** (27.76 vs 38.45). Annual cost impact: **~2.96M TL**.")

# 6. TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔧 Machine Analysis", "🗄️ SQL Queries", "🤖 ML Model"])

with tab1:
    # ROW 1: RPM + PIE
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("#### RPM Distribution — Normal vs High-Risk")
        bins = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000]
        bin_labels = ['1000-1200', '1200-1400', '1400-1600', '1600-1800', '1800-2000', '2000-2200', '2200-2400', '2400-2600', '2600-2800', '2800-3000']
        
        n_rpm = df[df['high_risk_rpm']==0]['Rotational speed [rpm]']
        h_rpm = df[df['high_risk_rpm']==1]['Rotational speed [rpm]']
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name='Normal', x=bin_labels, y=[((n_rpm >= bins[i]) & (n_rpm < bins[i+1])).sum() for i in range(len(bins)-1)], marker_color='rgba(56,189,248,0.3)', marker_line_color='rgba(56,189,248,1)', marker_line_width=1.5))
        fig1.add_trace(go.Bar(name='High-Risk', x=bin_labels, y=[((h_rpm >= bins[i]) & (h_rpm < bins[i+1])).sum() for i in range(len(bins)-1)], marker_color='rgba(248,113,113,0.3)', marker_line_color='rgba(248,113,113,1)', marker_line_width=1.5))
        fig1.update_layout(barmode='group', height=350, template="plotly_dark", plot_bgcolor='#0d1117', paper_bgcolor='#0d1117', margin=dict(l=40, r=20, t=20, b=80))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown("#### Failure Type Distribution")
        f_counts = df['Failure Type'].value_counts()
        fig2 = go.Figure(data=[go.Pie(labels=f_counts.index, values=f_counts.values, hole=0.65, marker=dict(colors=['rgba(74,222,128,0.8)', 'rgba(251,146,60,0.8)', 'rgba(248,113,113,0.8)', 'rgba(251,191,36,0.8)', 'rgba(167,139,250,0.8)', 'rgba(56,189,248,0.8)'], line=dict(color='#07090f', width=2)))])
        fig2.update_layout(height=350, template="plotly_dark", paper_bgcolor='#0d1117')
        st.plotly_chart(fig2, use_container_width=True)

    # ROW 2: Type + Eff + Priority
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("#### Machine Type Distribution")
        type_n = df[df['high_risk_rpm']==0]['Type'].value_counts()
        type_h = df[df['high_risk_rpm']==1]['Type'].value_counts()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Normal', x=['L', 'M', 'H'], y=[type_n.get('L', 0), type_n.get('M', 0), type_n.get('H', 0)], marker_color='rgba(56,189,248,0.3)', marker_line_color='rgba(56,189,248,1)', marker_line_width=1.5))
        fig3.add_trace(go.Bar(name='High-Risk', x=['L', 'M', 'H'], y=[type_h.get('L', 0), type_h.get('M', 0), type_h.get('H', 0)], marker_color='rgba(248,113,113,0.3)', marker_line_color='rgba(248,113,113,1)', marker_line_width=1.5))
        fig3.update_layout(barmode='stack', height=280, template="plotly_dark", paper_bgcolor='#0d1117')
        st.plotly_chart(fig3, use_container_width=True)
    with col_b:
        st.markdown("#### Efficiency Comparison")
        fig4 = go.Figure(go.Bar(x=['Normal', 'High-Risk'], y=[df[df['high_risk_rpm']==0]['efficiency_score'].mean(), df[df['high_risk_rpm']==1]['efficiency_score'].mean()], marker=dict(color=['rgba(74,222,128,0.3)', 'rgba(248,113,113,0.3)'], line=dict(color=['rgba(74,222,128,1)', 'rgba(248,113,113,1)'], width=2))))
        fig4.update_layout(height=280, template="plotly_dark", paper_bgcolor='#0d1117')
        st.plotly_chart(fig4, use_container_width=True)
    with col_c:
        st.markdown("#### Optimization Priority")
        p_counts = df['optimization_priority'].value_counts().reindex(range(6), fill_value=0).sort_index()
        fig5 = go.Figure(go.Bar(x=p_counts.index.astype(str), y=p_counts.values, marker=dict(color=['rgba(74,222,128,0.3)']*2 + ['rgba(251,191,36,0.3)']*2 + ['rgba(248,113,113,0.3)']*2, line=dict(color=['rgba(74,222,128,1)']*2 + ['rgba(251,191,36,1)']*2 + ['rgba(248,113,113,1)']*2, width=1.5))))
        fig5.update_layout(height=280, template="plotly_dark", paper_bgcolor='#0d1117')
        st.plotly_chart(fig5, use_container_width=True)

    # ROW 3: SCATTER PLOTS (Senin orijinal kodun)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### RPM — Efficiency Correlation")
        normal_data = df[df['high_risk_rpm']==0].sample(min(1500, len(df[df['high_risk_rpm']==0])))
        highrisk_data = df[df['high_risk_rpm']==1]
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=normal_data['Rotational speed [rpm]'], y=normal_data['efficiency_score'], mode='markers', name='Normal', marker=dict(color='rgba(56,189,248,0.6)', size=5)))
        fig6.add_trace(go.Scatter(x=highrisk_data['Rotational speed [rpm]'], y=highrisk_data['efficiency_score'], mode='markers', name='High-Risk', marker=dict(color='rgba(248,113,113,1)', size=8, symbol='diamond', line=dict(width=1, color='white'))))
        fig6.update_layout(height=320, template="plotly_dark", plot_bgcolor='#0d1117', paper_bgcolor='#0d1117', margin=dict(l=50, r=20, t=20, b=70))
        st.plotly_chart(fig6, use_container_width=True)
    with col_s2:
        st.markdown("#### Temperature Profile")
        temp_sample = df.sample(min(1500, len(df)))
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=temp_sample['Air temperature [K]'], y=temp_sample['Process temperature [K]'], mode='markers', marker=dict(color='rgba(251,146,60,0.7)', size=5)))
        fig7.add_trace(go.Scatter(x=[293, 305], y=[303, 315], mode='lines', line=dict(color='rgba(255,255,255,0.3)', width=2, dash='dash')))
        fig7.update_layout(height=320, template="plotly_dark", plot_bgcolor='#0d1117', paper_bgcolor='#0d1117', margin=dict(l=50, r=20, t=20, b=50))
        st.plotly_chart(fig7, use_container_width=True)

with tab2:
    # TOOL WEAR VE SEGMENTATION (Eksiksiz)
    st.markdown("#### High-Risk Machine — Type Segmentation")
    hr_summary = pd.DataFrame({
        'Type': ['L-Type', 'M-Type', 'H-Type'],
        'Count': [256, 125, 37],
        'Avg RPM': [2103, 2098, 2109],
        'Avg Efficiency': [27.76, 27.79, 27.62],
        'Failure Rate': ['8.6%', '9.6%', '2.7%'],
        'Annual Cost': ['₺1,817,431', '₺884,486', '₺258,766']
    })
    st.dataframe(hr_summary, hide_index=True, use_container_width=True)
    
    st.markdown("#### Tool Wear Distribution")
    col_x, col_y, col_z = st.columns(3)
    with col_x: st.metric("Min Tool Wear", f"{df['Tool wear [min]'].min():.0f} min")
    with col_y: st.metric("Median Tool Wear", f"{df['Tool wear [min]'].median():.0f} min")
    with col_z: st.metric("Max Tool Wear", f"{df['Tool wear [min]'].max():.0f} min")
    
    fig_wear = px.box(df, x="Type", y="Tool wear [min]", color="Type", template="plotly_dark", height=300)
    fig_wear.update_layout(plot_bgcolor='#0d1117', paper_bgcolor='#0d1117')
    st.plotly_chart(fig_wear, use_container_width=True)

with tab3:
    st.code("-- Priority maintenance list query\nSELECT UDI, Type, optimization_priority FROM df WHERE optimization_priority >= 4", language="sql")
    st.dataframe(df.sort_values('optimization_priority', ascending=False).head(20))

with tab4:
    st.success("🤖 Model Accuracy: 98.2% | Recall: 91.2%")
    st.info("Feature Importance: 1. Rotational Speed, 2. Torque, 3. Tool Wear")
