import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.graph_objs as go_objs

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
    
    # ────────────────────────────────────────────────
    # ROW 1: RPM Distribution + Failure Pie
    # ────────────────────────────────────────────────
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### RPM Distribution — Normal vs High-Risk")
        st.caption("IQR method · Threshold: 1139–1895 RPM")
        
        # Create bins manually
        bins = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000]
        bin_labels = ['1000-1200', '1200-1400', '1400-1600', '1600-1800', 
                     '1800-2000', '2000-2200', '2200-2400', '2400-2600', 
                     '2600-2800', '2800-3000']
        
        # Count machines in each bin
        normal_counts = []
        highrisk_counts = []
        
        normal_rpm = df[df['high_risk_rpm']==0]['Rotational speed [rpm]']
        highrisk_rpm = df[df['high_risk_rpm']==1]['Rotational speed [rpm]']
        
        for i in range(len(bins)-1):
            normal_counts.append(((normal_rpm >= bins[i]) & (normal_rpm < bins[i+1])).sum())
            highrisk_counts.append(((highrisk_rpm >= bins[i]) & (highrisk_rpm < bins[i+1])).sum())
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            name=f'Normal ({len(normal_rpm):,})',
            x=bin_labels,
            y=normal_counts,
            marker_color='rgba(56,189,248,0.3)',
            marker_line_color='rgba(56,189,248,1)',
            marker_line_width=1.5
        ))
        fig1.add_trace(go.Bar(
            name=f'High-Risk ({len(highrisk_rpm):,})',
            x=bin_labels,
            y=highrisk_counts,
            marker_color='rgba(248,113,113,0.3)',
            marker_line_color='rgba(248,113,113,1)',
            marker_line_width=1.5
        ))
        fig1.update_layout(
            barmode='group',
            height=350,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(
                gridcolor='#1e2738',
                title='RPM Range',
                color='#cdd9e5',
                tickangle=-45
            ),
            yaxis=dict(
                gridcolor='#1e2738',
                title='Machine Count',
                color='#cdd9e5'
            ),
            legend=dict(
                orientation='h',
                y=-0.25,
                font=dict(color='#cdd9e5')
            ),
            margin=dict(l=40, r=20, t=20, b=80)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Failure Type Distribution")
        st.caption("348 total failure records")
        
        failure_counts = df['Failure Type'].value_counts()
        
        fig2 = go.Figure(data=[go.Pie(
            labels=failure_counts.index,
            values=failure_counts.values,
            hole=0.65,
            marker=dict(
                colors=['rgba(74,222,128,0.8)', 'rgba(251,146,60,0.8)', 
                       'rgba(248,113,113,0.8)', 'rgba(251,191,36,0.8)', 
                       'rgba(167,139,250,0.8)', 'rgba(56,189,248,0.8)'],
                line=dict(color='#07090f', width=2)
            ),
            textposition='auto',
            textinfo='label+percent',
            textfont=dict(size=9, color='#cdd9e5'),
            hoverinfo='label+value+percent'
        )])
        fig2.update_layout(
            height=350,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=9),
            showlegend=True,
            legend=dict(
                orientation='v',
                x=1.05,
                y=0.5,
                font=dict(size=8, color='#cdd9e5')
            ),
            margin=dict(l=20, r=120, t=20, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────
    # ROW 2: Type + Efficiency + Priority
    # ────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Machine Type Distribution")
        st.caption("L / M / H type fleet")
        
        type_normal = df[df['high_risk_rpm']==0]['Type'].value_counts()
        type_highrisk = df[df['high_risk_rpm']==1]['Type'].value_counts()
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name='Normal',
            x=['L', 'M', 'H'],
            y=[type_normal.get('L', 0), type_normal.get('M', 0), type_normal.get('H', 0)],
            marker_color='rgba(56,189,248,0.3)',
            marker_line_color='rgba(56,189,248,1)',
            marker_line_width=1.5,
            text=[type_normal.get('L', 0), type_normal.get('M', 0), type_normal.get('H', 0)],
            textposition='inside',
            textfont=dict(color='#cdd9e5')
        ))
        fig3.add_trace(go.Bar(
            name='High-Risk',
            x=['L', 'M', 'H'],
            y=[type_highrisk.get('L', 0), type_highrisk.get('M', 0), type_highrisk.get('H', 0)],
            marker_color='rgba(248,113,113,0.3)',
            marker_line_color='rgba(248,113,113,1)',
            marker_line_width=1.5,
            text=[type_highrisk.get('L', 0), type_highrisk.get('M', 0), type_highrisk.get('H', 0)],
            textposition='inside',
            textfont=dict(color='#cdd9e5')
        ))
        fig3.update_layout(
            barmode='stack',
            height=280,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            legend=dict(orientation='h', y=-0.25, font=dict(color='#cdd9e5')),
            margin=dict(l=40, r=20, t=20, b=60)
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("#### Normal vs High-Risk Efficiency")
        st.caption("Efficiency Score comparison")
        
        normal_eff = df[df['high_risk_rpm']==0]['efficiency_score'].mean()
        highrisk_eff = df[df['high_risk_rpm']==1]['efficiency_score'].mean()
        
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=['Normal', 'High-Risk'],
            y=[normal_eff, highrisk_eff],
            marker=dict(
                color=['rgba(74,222,128,0.3)', 'rgba(248,113,113,0.3)'],
                line=dict(color=['rgba(74,222,128,1)', 'rgba(248,113,113,1)'], width=2)
            ),
            text=[f'{normal_eff:.2f}', f'{highrisk_eff:.2f}'],
            textposition='outside',
            textfont=dict(color='#cdd9e5', size=12)
        ))
        fig4.update_layout(
            height=280,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            yaxis=dict(
                gridcolor='#1e2738',
                range=[0, 45],
                color='#cdd9e5',
                title='Efficiency Score'
            ),
            showlegend=False,
            margin=dict(l=40, r=20, t=20, b=40)
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with col3:
        st.markdown("#### Optimization Priority Distribution")
        st.caption("Score 0–5 · 418 critical (4-5)")
        
        priority_counts = df['optimization_priority'].value_counts().reindex(range(6), fill_value=0).sort_index()
        
        colors = ['rgba(74,222,128,0.3)'] * 2 + ['rgba(251,191,36,0.3)'] * 2 + ['rgba(248,113,113,0.3)'] * 2
        borders = ['rgba(74,222,128,1)'] * 2 + ['rgba(251,191,36,1)'] * 2 + ['rgba(248,113,113,1)'] * 2
        
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=priority_counts.index.astype(str),
            y=priority_counts.values,
            marker=dict(
                color=colors,
                line=dict(color=borders, width=1.5)
            ),
            text=priority_counts.values,
            textposition='outside',
            textfont=dict(color='#cdd9e5')
        ))
        fig5.update_layout(
            height=280,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(
                gridcolor='#1e2738',
                title='Priority',
                color='#cdd9e5'
            ),
            yaxis=dict(
                gridcolor='#1e2738',
                title='Count',
                color='#cdd9e5'
            ),
            showlegend=False,
            margin=dict(l=40, r=20, t=20, b=40)
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        st.caption("🟢 0-1: Normal | 🟡 2-3: Monitor | 🔴 4-5: URGENT")
    
    st.markdown("<br>", unsafe_allow_html=True)
    

# ────────────────────────────────────────────────
    # ROW 3: Correlation Scatter
    # ────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### RPM — Efficiency Correlation")
        st.caption("High RPM = Low Efficiency")
        
        # Prepare data
        normal_data = df[df['high_risk_rpm']==0].sample(min(1500, len(df[df['high_risk_rpm']==0])))
        highrisk_data = df[df['high_risk_rpm']==1]
        
        fig6 = go.Figure()
        
        # Normal machines - LARGER & MORE VISIBLE
        fig6.add_trace(go.Scatter(
            x=normal_data['Rotational speed [rpm]'],
            y=normal_data['efficiency_score'],
            mode='markers',
            name=f'Normal ({len(normal_data):,})',
            marker=dict(
                color='rgba(56,189,248,0.6)',  # More opaque
                size=5,  # Larger
                line=dict(width=0)
            ),
            hovertemplate='<b>Normal</b><br>RPM: %{x:.0f}<br>Efficiency: %{y:.2f}<extra></extra>'
        ))
        
        # High-risk machines - VERY VISIBLE
        fig6.add_trace(go.Scatter(
            x=highrisk_data['Rotational speed [rpm]'],
            y=highrisk_data['efficiency_score'],
            mode='markers',
            name=f'High-Risk ({len(highrisk_data):,})',
            marker=dict(
                color='rgba(248,113,113,1)',  # Fully opaque
                size=8,  # Much larger
                symbol='diamond',
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>High-Risk</b><br>RPM: %{x:.0f}<br>Efficiency: %{y:.2f}<extra></extra>'
        ))
        
        fig6.update_layout(
            height=320,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(
                gridcolor='#1e2738',
                title='Rotational Speed (RPM)',
                color='#cdd9e5',
                range=[1000, 3000],
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='#1e2738',
                title='Efficiency Score',
                color='#cdd9e5',
                range=[15, 50],
                showgrid=True
            ),
            legend=dict(
                orientation='h',
                y=-0.2,
                x=0.5,
                xanchor='center',
                font=dict(color='#cdd9e5', size=9),
                bgcolor='rgba(13,17,23,0.8)'
            ),
            margin=dict(l=50, r=20, t=20, b=70),
            hovermode='closest'
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        st.markdown("#### Temperature Profile (Air vs Process)")
        st.caption("Kelvin distribution")
        
        # Sample data
        temp_sample = df.sample(min(1500, len(df)))
        
        fig7 = go.Figure()
        
        # Temperature points - LARGER & MORE VISIBLE
        fig7.add_trace(go.Scatter(
            x=temp_sample['Air temperature [K]'],
            y=temp_sample['Process temperature [K]'],
            mode='markers',
            marker=dict(
                color='rgba(251,146,60,0.7)',  # More opaque
                size=5,  # Larger
                line=dict(width=0)
            ),
            showlegend=False,
            hovertemplate='Air: %{x:.1f}K<br>Process: %{y:.1f}K<extra></extra>'
        ))
        
        # Diagonal reference line - MORE VISIBLE
        fig7.add_trace(go.Scatter(
            x=[293, 305],
            y=[303, 315],
            mode='lines',
            line=dict(
                color='rgba(255,255,255,0.3)',  # Brighter
                width=2,  # Thicker
                dash='dash'
            ),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig7.update_layout(
            height=320,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(
                gridcolor='#1e2738',
                title='Air Temperature (K)',
                color='#cdd9e5',
                range=[293, 305],
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='#1e2738',
                title='Process Temperature (K)',
                color='#cdd9e5',
                range=[303, 315],
                showgrid=True
            ),
            margin=dict(l=50, r=20, t=20, b=50),
            hovermode='closest'
        )
        st.plotly_chart(fig7, use_container_width=True)




# ═══════════════════════════════════════════════════
# TAB 2: MACHINE ANALYSIS
# ═══════════════════════════════════════════════════
with tab2:
    
    # KPI Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🔴 High-Risk Machines",
            value="418",
            delta="4.18% of fleet"
        )
    
    with col2:
        st.metric(
            label="🟡 Bottom 10% (Inefficient)",
            value="1,000",
            delta="20.5% lower efficiency"
        )
    
    with col3:
        st.metric(
            label="💰 Max Annual Savings",
            value="227K TL",
            delta="50% failure reduction"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # High-Risk Segmentation Table
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### High-Risk Machine — Type Segmentation")
        st.caption("Failure rate and cost analysis")
        
        # Create summary table
        highrisk_summary = pd.DataFrame({
            'Type': ['L-Type', 'M-Type', 'H-Type'],
            'Count': [256, 125, 37],
            'Avg RPM': [2103, 2098, 2109],
            'Avg Efficiency': [27.76, 27.79, 27.62],
            'Failure Rate': ['8.6%', '9.6%', '2.7%'],
            'Annual Cost': ['₺1,817,431', '₺884,486', '₺258,766']
        })
        
        st.dataframe(
            highrisk_summary,
            hide_index=True,
            use_container_width=True,
            height=180
        )
        
        st.info("⚡ **Priority:** L-type (volume), M-type (risk 9.6%), H-type (low risk)")
    
    with col2:
        st.markdown("#### High-Risk Distribution by Type")
        st.caption("418 machines breakdown")
        
        highrisk_by_type = df[df['high_risk_rpm']==1]['Type'].value_counts()
        
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Bar(
            x=['L-Type', 'M-Type', 'H-Type'],
            y=highrisk_by_type.values,
            marker=dict(
                color=['rgba(248,113,113,0.3)', 'rgba(251,146,60,0.3)', 'rgba(56,189,248,0.3)'],
                line=dict(color=['#f87171', '#fb923c', '#38bdf8'], width=2)
            ),
            text=highrisk_by_type.values,
            textposition='outside',
            textfont=dict(color='#cdd9e5', size=14)
        ))
        fig_hr.update_layout(
            height=280,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', title='Machine Count', color='#cdd9e5'),
            showlegend=False,
            margin=dict(l=50, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_hr, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Energy Category + Tool Wear
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Energy Category Distribution")
        st.caption("Power consumption segmentation")
        
        # Define categories based on actual data
        def categorize_energy(power):
            if power < 0.8:
                return 'Low'
            elif power < 1.2:
                return 'Medium'
            else:
                return 'High'
        
        df['energy_category'] = df['power_consumption_kw'].apply(categorize_energy)
        energy_counts = df['energy_category'].value_counts()
        
        # Show actual counts
        st.write(f"**Breakdown:**")
        st.write(f"- Low (<0.8 kW): {energy_counts.get('Low', 0):,} machines")
        st.write(f"- Medium (0.8-1.2 kW): {energy_counts.get('Medium', 0):,} machines")
        st.write(f"- High (>1.2 kW): {energy_counts.get('High', 0):,} machines")
        
        fig_energy = go.Figure(data=[go.Pie(
            labels=energy_counts.index,
            values=energy_counts.values,
            hole=0.6,
            marker=dict(
                colors=['rgba(248,113,113,0.7)', 'rgba(56,189,248,0.7)', 'rgba(74,222,128,0.7)'],
                line=dict(color='#07090f', width=2)
            ),
            textposition='inside',
            textinfo='label+percent',
            textfont=dict(size=11, color='#cdd9e5', weight='bold'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
        )])
        fig_energy.update_layout(
            height=240,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            showlegend=True,
            legend=dict(
                orientation='h',
                y=-0.1,
                x=0.5,
                xanchor='center',
                font=dict(size=9, color='#cdd9e5')
            ),
            margin=dict(l=20, r=20, t=10, b=40)
        )
        st.plotly_chart(fig_energy, use_container_width=True)
        
        # High-risk breakdown
        highrisk_energy = df[df['high_risk_rpm']==1]['energy_category'].value_counts()
        low_pct = (highrisk_energy.get('Low', 0) / 418 * 100) if len(highrisk_energy) > 0 else 0
        
        st.caption(f"⚠️ **High-Risk:** {low_pct:.1f}% are 'Low' category (misleading - low torque causes low power calculation)")
```

---

## 🔑 KRİTİK DEĞİŞİKLİKLER:

1. **Manuel kategorileme:** `apply(categorize_energy)` ile gerçek değerler
2. **Sayıları göster:** Text olarak breakdown eklendi
3. **High-risk breakdown:** 97.6% doğrulaması eklendi
4. **Hover bilgisi:** Sayıları görmek için tooltip

---

## ❓ BEKLENEN SONUÇ:

**Gerçek dağılım muhtemelen:**
```
Low: ~874 (%8.7)
Medium: ~7,362 (%73.6)
High: ~1,764 (%17.6)
    
    with col2:
        st.markdown("#### Tool Wear Distribution")
        st.caption("Average: 107.95 minutes")
        
        wear_bins = pd.cut(df['Tool wear [min]'], bins=5)
        wear_counts = wear_bins.value_counts().sort_index()
        
        fig_wear = go.Figure()
        fig_wear.add_trace(go.Bar(
            x=[str(x) for x in wear_counts.index],
            y=wear_counts.values,
            marker_color='rgba(251,146,60,0.3)',
            marker_line_color='#fb923c',
            marker_line_width=1.5
        ))
        fig_wear.update_layout(
            height=300,
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(
                gridcolor='#1e2738',
                title='Tool Wear Range (min)',
                color='#cdd9e5',
                tickangle=-45
            ),
            yaxis=dict(gridcolor='#1e2738', title='Machine Count', color='#cdd9e5'),
            showlegend=False,
            margin=dict(l=50, r=20, t=20, b=80)
        )
        st.plotly_chart(fig_wear, use_container_width=True)
