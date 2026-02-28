import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="⚡ Energy Efficiency Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'page' not in st.session_state:
    st.session_state.page = 'cover'

@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/Nisanuraltay/manufacturing-energy-efficiency/main/data/predictive_maintenance_final_data.csv'
    try:
        df = pd.read_csv(url)
    except:
        df = pd.read_csv('data/predictive_maintenance_final_data.csv')
    df['Rotational speed [rpm]'] = df['Rotational speed [rpm]'].astype(float)
    df['Torque [Nm]'] = df['Torque [Nm]'].astype(float)
    df['Tool wear [min]'] = df['Tool wear [min]'].astype(float)
    df['Target'] = df['Target'].astype(float)
    df['temp_difference'] = df['Process temperature [K]'] - df['Air temperature [K]']
    rpm = df['Rotational speed [rpm]']
    Q1, Q3 = rpm.quantile(0.25), rpm.quantile(0.75)
    IQR = Q3 - Q1
    df['high_risk_rpm'] = ((rpm < Q1 - 1.5*IQR) | (rpm > Q3 + 1.5*IQR)).astype(int)
    df['power_consumption_kw'] = (df['Rotational speed [rpm]'] / 1000) * (df['Torque [Nm]'] / 100) * 1.73
    df['efficiency_score'] = df['Torque [Nm]'] / df['power_consumption_kw']
    df['cost_per_hour_tl'] = df['power_consumption_kw'] * 1.2
    def calc_priority(row):
        score = 0
        if row['high_risk_rpm'] == 1: score += 2
        if row['efficiency_score'] < df['efficiency_score'].median(): score += 2
        if row['Target'] == 1: score += 1
        return min(score, 5)
    df['optimization_priority'] = df.apply(calc_priority, axis=1)
    def categorize_energy(power):
        if power < 0.8: return 'Low'
        elif power < 1.2: return 'Medium'
        else: return 'High'
    df['energy_category'] = df['power_consumption_kw'].apply(categorize_energy)
    wear_bins = [0, 50, 100, 150, 200, 253]
    wear_labels = ['0-50', '50-100', '100-150', '150-200', '200-253']
    df['wear_bin'] = pd.cut(df['Tool wear [min]'], bins=wear_bins, labels=wear_labels, include_lowest=True)
    return df

# ═══════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════
if st.session_state.page == 'cover':
    st.markdown("""
    <style>
    .stApp { background: #000 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header { display: none !important; }
    footer { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:80px;filter:drop-shadow(0 0 40px rgba(255,165,0,0.6))'>⚡</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:12px;letter-spacing:8px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin:16px 0'>INDUSTRIAL DATA SCIENCE PORTFOLIO</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:4px;background:linear-gradient(90deg,transparent,#ff8c00,#ffaa00,#ff8c00,transparent);box-shadow:0 0 20px rgba(255,140,0,0.4);margin:0 auto;max-width:700px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:48px;font-weight:900;letter-spacing:4px;text-transform:uppercase;color:#fff;line-height:1.2'>MANUFACTURING ENERGY<br><span style=\"color:#ffaa00\">EFFICIENCY ANALYSIS</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:16px;color:rgba(255,255,255,0.5);font-style:italic'>Predictive Maintenance · Machine Learning · SQL Analytics<br><span style=\"color:rgba(255,165,0,0.8);font-weight:600\">\"10,000 Machines · 418 High-Risk · 227K TL Savings\"</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center'><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,140,0,0.4);color:rgba(255,140,0,0.8);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>PYTHON</span><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.4);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>SQL</span><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.4);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>RANDOM FOREST</span><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.4);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>STREAMLIT</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 ENTER DASHBOARD", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    st.markdown("<div style='text-align:center;margin-top:40px;font-size:11px;color:rgba(255,255,255,0.2);letter-spacing:3px;text-transform:uppercase'>N. Nur Altay · Data Analyst · February 2026</div>", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════
# DASHBOARD — GLOBAL CSS
# ═══════════════════════════════════════════
st.markdown("""
<style>
.stApp { background: #07090f !important; color: #cdd9e5 !important; }
section[data-testid="stMain"] { background: #07090f !important; }
.block-container { background: #07090f !important; padding-top: 1rem; padding-bottom: 1rem; max-width: 100% !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #0a0e1a !important;
    border-right: 1px solid rgba(0,206,209,0.15) !important;
    min-width: 220px !important;
    max-width: 220px !important;
}
section[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* Metrics */
[data-testid="metric-container"] { background: #0d1117 !important; border: 1px solid #1e2738 !important; border-radius: 10px !important; padding: 12px !important; }
[data-testid="stMetricValue"] { color: #cdd9e5 !important; font-size: 20px !important; }
[data-testid="stMetricLabel"] { color: #4a6072 !important; font-size: 11px !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #0d1117 !important; border: 1px solid #1e2738 !important; border-radius: 8px !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { color: #4a6072 !important; border-radius: 6px !important; padding: 8px 16px !important; font-size: 12px !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { background: #161b24 !important; color: #00ced1 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #07090f !important; padding-top: 16px !important; }

/* Expander */
[data-testid="stExpander"] { background: #0d1117 !important; border: 1px solid #1e2738 !important; border-radius: 10px !important; }
summary { color: #cdd9e5 !important; }
pre { background: #0d1117 !important; color: #cdd9e5 !important; }

/* Text */
p, h1, h2, h3, h4, label, div { color: #cdd9e5; }
.stCaption > div { color: #4a6072 !important; }
[data-testid="stAlert"] { background: #0d1117 !important; border-color: #1e2738 !important; }

/* Multiselect / Select */
[data-baseweb="select"] { background: #0d1117 !important; border-color: #1e2738 !important; }
[data-baseweb="tag"] { background: rgba(0,206,209,0.15) !important; color: #00ced1 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; background: #07090f; }
::-webkit-scrollbar-thumb { background: #1e2738; border-radius: 2px; }
header[data-testid="stHeader"] { background: #07090f !important; border-bottom: 1px solid #1e2738 !important; }
footer { display: none !important; }

/* Enter button override */
.stButton > button {
    background: linear-gradient(135deg, #00ced1, #0891b2) !important;
    color: #000 !important; font-weight: 700 !important;
    border-radius: 8px !important; border: none !important;
    font-size: 12px !important; padding: 8px 20px !important;
}
</style>
""", unsafe_allow_html=True)

df = load_data()

# ═══════════════════════════════════════════
# SIDEBAR NAVIGATOR + FILTERS
# ═══════════════════════════════════════════
with st.sidebar:
    # Logo / Title
    st.markdown("""
    <div style="padding:20px 16px 12px;border-bottom:1px solid rgba(0,206,209,0.15)">
        <div style="font-size:22px;margin-bottom:4px">⚡</div>
        <div style="font-size:13px;font-weight:800;color:#00ced1;letter-spacing:1px;text-transform:uppercase">Energy Dashboard</div>
        <div style="font-size:9px;color:rgba(255,255,255,0.25);letter-spacing:2px;text-transform:uppercase;margin-top:2px">N. Nur Altay · Feb 2026</div>
    </div>
    """, unsafe_allow_html=True)

    # Fleet Stats
    st.markdown("""
    <div style="padding:12px 16px 8px">
        <div style="font-size:8px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.2);margin-bottom:8px;font-weight:700">FLEET OVERVIEW</div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("🏭 Total", f"{len(df):,}")
        st.metric("✅ Normal", f"{len(df)-df['high_risk_rpm'].sum():,}")
    with col_b:
        st.metric("⚠️ Risk", f"{df['high_risk_rpm'].sum()}")
        st.metric("🔥 Fail", f"{int(df['Target'].sum())}")

    st.markdown("<hr style='border-color:rgba(0,206,209,0.1);margin:8px 0'>", unsafe_allow_html=True)

    # FILTERS
    st.markdown("""
    <div style="padding:4px 0 8px">
        <div style="font-size:8px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.2);margin-bottom:10px;font-weight:700">FILTERS</div>
    </div>
    """, unsafe_allow_html=True)

    # Machine Type Filter
    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px'>Machine Type</div>", unsafe_allow_html=True)
    type_filter = st.multiselect(
        label="type",
        options=['L', 'M', 'H'],
        default=['L', 'M', 'H'],
        label_visibility="collapsed"
    )

    # Risk Filter
    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;margin-top:8px'>Risk Status</div>", unsafe_allow_html=True)
    risk_filter = st.multiselect(
        label="risk",
        options=['Normal', 'High-Risk'],
        default=['Normal', 'High-Risk'],
        label_visibility="collapsed"
    )

    # Priority Filter
    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;margin-top:8px'>Priority Score</div>", unsafe_allow_html=True)
    priority_range = st.select_slider(
        label="priority",
        options=[0, 1, 2, 3, 4, 5],
        value=(0, 5),
        label_visibility="collapsed"
    )

    # RPM Range
    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;margin-top:8px'>RPM Range</div>", unsafe_allow_html=True)
    rpm_min = int(df['Rotational speed [rpm]'].min())
    rpm_max = int(df['Rotational speed [rpm]'].max())
    rpm_range = st.slider(
        label="rpm",
        min_value=rpm_min,
        max_value=rpm_max,
        value=(rpm_min, rpm_max),
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:rgba(0,206,209,0.1);margin:8px 0'>", unsafe_allow_html=True)

    # Cost Info
    st.markdown("""
    <div style="padding:4px 0 8px">
        <div style="font-size:8px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.2);margin-bottom:10px;font-weight:700">COST SNAPSHOT</div>
    </div>
    """, unsafe_allow_html=True)

    total_annual = df['cost_per_hour_tl'].sum() * 24 * 365
    highrisk_annual = df[df['high_risk_rpm']==1]['cost_per_hour_tl'].sum() * 24 * 365

    st.markdown(f"""
    <div style="background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.15);border-radius:8px;padding:10px 12px;margin-bottom:6px">
        <div style="font-size:14px;font-weight:800;color:#f87171">₺{highrisk_annual/1e6:.2f}M</div>
        <div style="font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:1px">High-Risk Cost/yr</div>
    </div>
    <div style="background:rgba(0,206,209,0.06);border:1px solid rgba(0,206,209,0.15);border-radius:8px;padding:10px 12px;margin-bottom:6px">
        <div style="font-size:14px;font-weight:800;color:#00ced1">₺{total_annual/1e6:.1f}M</div>
        <div style="font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:1px">Total Fleet Cost/yr</div>
    </div>
    <div style="background:rgba(74,222,128,0.06);border:1px solid rgba(74,222,128,0.15);border-radius:8px;padding:10px 12px">
        <div style="font-size:14px;font-weight:800;color:#4ade80">₺227K</div>
        <div style="font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:1px">Savings Potential</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(0,206,209,0.1);margin:8px 0'>", unsafe_allow_html=True)

    # Back to cover
    if st.button("← Back to Cover", use_container_width=True):
        st.session_state.page = 'cover'
        st.rerun()

# ═══════════════════════════════════════════
# APPLY FILTERS
# ═══════════════════════════════════════════
risk_map = []
if 'Normal' in risk_filter: risk_map.append(0)
if 'High-Risk' in risk_filter: risk_map.append(1)

dff = df[
    (df['Type'].isin(type_filter)) &
    (df['high_risk_rpm'].isin(risk_map)) &
    (df['optimization_priority'] >= priority_range[0]) &
    (df['optimization_priority'] <= priority_range[1]) &
    (df['Rotational speed [rpm]'] >= rpm_range[0]) &
    (df['Rotational speed [rpm]'] <= rpm_range[1])
]

# ═══════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════
filtered_note = f"Showing **{len(dff):,}** of {len(df):,} machines" if len(dff) != len(df) else f"All **{len(df):,}** machines"

st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d1117,#161b24);border:1px solid #1e2738;border-radius:12px;padding:16px 24px;margin-bottom:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
        <div style="display:flex;align-items:center;gap:16px">
            <div style="width:44px;height:44px;background:linear-gradient(135deg,#00ced1,#0891b2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 0 16px rgba(0,206,209,0.3)">⚡</div>
            <div>
                <div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:-0.3px">Manufacturing Energy Efficiency Analysis</div>
                <div style="font-size:10px;color:#4a6072;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px">Predictive Maintenance · 10,000 Machines · N.Nur Altay</div>
            </div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
            <div style="padding:6px 12px;background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.2);border-radius:16px;font-size:10px;color:#4ade80;display:flex;align-items:center;gap:6px">
                <div style="width:6px;height:6px;background:#4ade80;border-radius:50%"></div>Live Dashboard
            </div>
            <div style="padding:6px 12px;background:#161b24;border:1px solid #1e2738;border-radius:16px;font-size:10px;color:#4a6072">Feb 2026</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric("🏭 Machines", f"{len(dff):,}", delta=f"{len(dff)/len(df)*100:.0f}% of fleet")
with c2:
    hr = dff['high_risk_rpm'].sum()
    st.metric("⚠️ High-Risk", f"{hr}", delta=f"{hr/len(dff)*100:.1f}%" if len(dff)>0 else "0%", delta_color="inverse")
with c3:
    ne = dff[dff['high_risk_rpm']==0]['efficiency_score'].mean() if len(dff)>0 else 0
    st.metric("📈 Avg Efficiency", f"{ne:.1f}" if ne else "—")
with c4:
    st.metric("💰 Avg Cost", f"{dff['cost_per_hour_tl'].mean():.2f} TL/hr" if len(dff)>0 else "—")
with c5:
    fl = int(dff['Target'].sum())
    st.metric("🔥 Failures", f"{fl}", delta=f"{fl/len(dff)*100:.1f}%" if len(dff)>0 else "0%", delta_color="inverse")

if len(dff) != len(df):
    st.info(f"🔍 **Filter Active:** {filtered_note} | Types: {', '.join(type_filter)} | Risk: {', '.join(risk_filter)} | Priority: {priority_range[0]}–{priority_range[1]} | RPM: {rpm_range[0]}–{rpm_range[1]}")
else:
    st.info("💡 **Key Finding:** 418 high-risk machines have **27.8% lower efficiency** (27.76 vs 38.45). Annual cost impact: **~2.96M TL**. Use sidebar filters to explore.")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔧 Machine Analysis", "🗄️ SQL Queries", "🤖 ML Model"])

# ═══════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════
with tab1:

    components.html("""
<!DOCTYPE html><html><head><style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#07090f; font-family:'Segoe UI',sans-serif; }
.slider-wrap { width:100%; overflow:hidden; background:#07090f; }
.slides { display:flex; transition:transform 0.5s cubic-bezier(0.4,0,0.2,1); }
.slide { min-width:100%; padding:32px 40px; position:relative; overflow:hidden; }
.slide-1{background:linear-gradient(135deg,#0a0e1a,#0d1525);}
.slide-2{background:linear-gradient(135deg,#100a08,#1a0e0a);}
.slide-3{background:linear-gradient(135deg,#080d10,#0a1218);}
.slide-4{background:linear-gradient(135deg,#08100a,#0a1410);}
.slide-5{background:linear-gradient(135deg,#0d0a14,#120d1c);}
.slide-num{position:absolute;top:20px;right:32px;font-size:64px;font-weight:900;color:rgba(255,255,255,0.04);letter-spacing:-4px;line-height:1;user-select:none;}
.slide-label{font-size:9px;letter-spacing:4px;text-transform:uppercase;margin-bottom:10px;font-weight:700;}
.label-blue{color:#38bdf8;}.label-red{color:#f87171;}.label-cyan{color:#00e5d4;}.label-green{color:#4ade80;}.label-purple{color:#a78bfa;}
.slide-title{font-size:24px;font-weight:800;color:#fff;line-height:1.2;margin-bottom:6px;letter-spacing:-0.5px;}
.slide-title span{color:#ffaa00;}
.divider{width:40px;height:3px;border-radius:2px;margin:12px 0;}
.div-blue{background:#38bdf8;}.div-red{background:#f87171;}.div-cyan{background:#00e5d4;}.div-green{background:#4ade80;}.div-purple{background:#a78bfa;}
.kpi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px;}
.kpi-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:14px;text-align:center;}
.kpi-val{font-size:22px;font-weight:900;line-height:1;margin-bottom:3px;}
.kpi-lbl{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.3);}
.insight-row{display:flex;align-items:flex-start;gap:10px;padding:12px 14px;background:rgba(255,255,255,0.03);border-left:3px solid;border-radius:0 8px 8px 0;margin-bottom:8px;}
.insight-icon{font-size:18px;flex-shrink:0;margin-top:2px;}
.insight-title{font-size:12px;font-weight:700;color:#fff;margin-bottom:2px;}
.insight-desc{font-size:10px;color:rgba(255,255,255,0.45);line-height:1.5;}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px;}
.action-item{display:flex;align-items:center;gap:10px;padding:10px 14px;background:rgba(255,255,255,0.03);border-radius:8px;margin-bottom:6px;}
.action-badge{font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;border-radius:4px;flex-shrink:0;min-width:64px;text-align:center;}
.badge-red{background:rgba(248,113,113,0.15);color:#f87171;border:1px solid rgba(248,113,113,0.3);}
.badge-orange{background:rgba(251,146,60,0.15);color:#fb923c;border:1px solid rgba(251,146,60,0.3);}
.badge-yellow{background:rgba(251,191,36,0.15);color:#fbbf24;border:1px solid rgba(251,191,36,0.3);}
.badge-green{background:rgba(74,222,128,0.15);color:#4ade80;border:1px solid rgba(74,222,128,0.3);}
.action-text{font-size:11px;color:rgba(255,255,255,0.7);}
.action-impact{font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px;}
.slide-desc{font-size:12px;color:rgba(255,255,255,0.45);line-height:1.7;margin-top:10px;max-width:600px;}
.nav{display:flex;align-items:center;justify-content:space-between;padding:12px 40px 16px;background:#07090f;border-top:1px solid rgba(255,255,255,0.06);}
.nav-dots{display:flex;gap:6px;align-items:center;}
.dot{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.15);cursor:pointer;transition:all 0.3s;}
.dot.active{background:#ffaa00;width:20px;border-radius:4px;}
.nav-btn{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.6);padding:7px 18px;border-radius:7px;font-size:11px;font-weight:600;cursor:pointer;transition:all 0.2s;}
.nav-btn:hover{background:rgba(255,255,255,0.1);color:#fff;}
.nav-btn:disabled{opacity:0.2;cursor:default;}
.nav-counter{font-size:10px;color:rgba(255,255,255,0.25);letter-spacing:2px;font-weight:600;}
</style></head><body>
<div class="slider-wrap"><div class="slides" id="slides">

<div class="slide slide-1">
  <div class="slide-num">01</div>
  <div class="slide-label label-blue">EXECUTIVE SUMMARY</div>
  <div class="slide-title">Manufacturing Energy Efficiency<br><span>Analysis Overview</span></div>
  <div class="divider div-blue"></div>
  <div class="slide-desc">End-to-end analysis of 10,000 production machines to identify energy inefficiencies, quantify financial risk, and build a predictive ML model for proactive maintenance prioritization.</div>
  <div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-val" style="color:#38bdf8">10,000</div><div class="kpi-lbl">Machines Analyzed</div></div>
    <div class="kpi-card"><div class="kpi-val" style="color:#f87171">418</div><div class="kpi-lbl">High-Risk Units</div></div>
    <div class="kpi-card"><div class="kpi-val" style="color:#4ade80">100%</div><div class="kpi-lbl">ML Accuracy</div></div>
    <div class="kpi-card"><div class="kpi-val" style="color:#ffaa00">₺2.96M</div><div class="kpi-lbl">Annual Cost Risk</div></div>
    <div class="kpi-card"><div class="kpi-val" style="color:#a78bfa">227K TL</div><div class="kpi-lbl">Savings Potential</div></div>
    <div class="kpi-card"><div class="kpi-val" style="color:#fb923c">3</div><div class="kpi-lbl">Analysis Phases</div></div>
  </div>
</div>

<div class="slide slide-2">
  <div class="slide-num">02</div>
  <div class="slide-label label-red">BUSINESS PROBLEM</div>
  <div class="slide-title">The Cost of <span>Undetected Inefficiency</span></div>
  <div class="divider div-red"></div>
  <div style="margin-top:16px">
    <div class="insight-row" style="border-color:#f87171"><div class="insight-icon">⚠️</div><div><div class="insight-title">Hidden High-Risk Machines</div><div class="insight-desc">418 machines (4.18% of fleet) operate at abnormal RPM — undetected without data analysis. 2.6× higher failure rate than normal units.</div></div></div>
    <div class="insight-row" style="border-color:#fb923c"><div class="insight-icon">💸</div><div><div class="insight-title">₺2.96M Annual Cost Impact</div><div class="insight-desc">High-risk machines generate ₺454,826/year in failure costs. L-type machines drive 60% of total fleet energy cost (₺65.5M/year).</div></div></div>
    <div class="insight-row" style="border-color:#fbbf24"><div class="insight-icon">📉</div><div><div class="insight-title">27.8% Efficiency Gap</div><div class="insight-desc">High-risk machines score 27.76 vs 38.45 efficiency average — a 27.8% gap translating to wasted energy and increased operational cost.</div></div></div>
  </div>
</div>

<div class="slide slide-3">
  <div class="slide-num">03</div>
  <div class="slide-label label-cyan">KEY FINDINGS</div>
  <div class="slide-title">What the Data <span>Revealed</span></div>
  <div class="divider div-cyan"></div>
  <div class="two-col">
    <div>
      <div style="font-size:9px;letter-spacing:2px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:10px">Machine Risk Profile</div>
      <div class="insight-row" style="border-color:#00e5d4;margin-bottom:6px"><div><div class="insight-title" style="font-size:11px">High RPM + Low Torque</div><div class="insight-desc">Avg RPM: 2,102 vs 1,514 (normal). Avg Torque: 18.9 Nm vs 40.9 Nm → 54% lower.</div></div></div>
      <div class="insight-row" style="border-color:#f87171"><div><div class="insight-title" style="font-size:11px">Failure Rate: 8.37% vs 3.17%</div><div class="insight-desc">High-risk machines fail 2.6× more. M-type carries highest risk at 9.6%.</div></div></div>
    </div>
    <div>
      <div style="font-size:9px;letter-spacing:2px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:10px">Fleet Breakdown</div>
      <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:14px">
        <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06)"><span style="font-size:11px;color:rgba(255,255,255,0.6)">L-Type</span><span style="font-size:11px;font-weight:700;color:#f87171">256 units · 8.6% fail</span></div>
        <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06)"><span style="font-size:11px;color:rgba(255,255,255,0.6)">M-Type</span><span style="font-size:11px;font-weight:700;color:#fb923c">125 units · 9.6% fail</span></div>
        <div style="display:flex;justify-content:space-between;padding:7px 0"><span style="font-size:11px;color:rgba(255,255,255,0.6)">H-Type</span><span style="font-size:11px;font-weight:700;color:#4ade80">37 units · 2.7% fail</span></div>
        <div style="margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06)"><div style="font-size:9px;color:rgba(255,255,255,0.3);margin-bottom:4px">NIGHT SHIFT RISK</div><div style="font-size:12px;font-weight:700;color:#fbbf24">100% of high-risk → Night Shift</div></div>
      </div>
    </div>
  </div>
</div>

<div class="slide slide-4">
  <div class="slide-num">04</div>
  <div class="slide-label label-green">SQL BUSINESS INSIGHTS</div>
  <div class="slide-title">3 Queries That <span>Changed the Strategy</span></div>
  <div class="divider div-green"></div>
  <div style="margin-top:16px">
    <div class="insight-row" style="border-color:#4ade80"><div class="insight-icon">🔵</div><div><div class="insight-title">Query 1 — Cost by Machine Type</div><div class="insight-desc">L-type: ₺65.5M/yr (60%) · M-type: ₺32.7M/yr · H-type: ₺10.9M/yr → <strong style="color:#4ade80">L-type = highest ROI target</strong></div></div></div>
    <div class="insight-row" style="border-color:#fbbf24"><div class="insight-icon">🔴</div><div><div class="insight-title">Query 2 — Bottom 10% Efficiency</div><div class="insight-desc">1,000 critically inefficient machines — 47% below fleet average → <strong style="color:#fbbf24">₺454K/yr recovery potential</strong></div></div></div>
    <div class="insight-row" style="border-color:#fb923c"><div class="insight-icon">🟠</div><div><div class="insight-title">Query 3 — High-Risk Segmentation</div><div class="insight-desc">M-type: 9.6% failure rate — highest per-unit risk → <strong style="color:#fb923c">Risk mitigation program needed</strong></div></div></div>
  </div>
</div>

<div class="slide slide-5">
  <div class="slide-num">05</div>
  <div class="slide-label label-purple">STRATEGIC ACTION PLAN</div>
  <div class="slide-title">4-Step <span>Optimization Roadmap</span></div>
  <div class="divider div-purple"></div>
  <div style="margin-top:16px">
    <div class="action-item"><div class="action-badge badge-red">URGENT</div><div><div class="action-text">Bottom 10% Immediate Maintenance — 1,000 machines</div><div class="action-impact">Timeline: Immediately · Impact: ₺454K/yr savings</div></div></div>
    <div class="action-item"><div class="action-badge badge-orange">30 DAYS</div><div><div class="action-text">L-Type RPM Optimization — 256 high-risk units</div><div class="action-impact">Timeline: 30 days · Impact: Highest ROI (60% of cost base)</div></div></div>
    <div class="action-item"><div class="action-badge badge-yellow">60 DAYS</div><div><div class="action-text">M-Type Failure Prevention Program — 9.6% failure rate</div><div class="action-impact">Timeline: 60 days · Impact: Risk mitigation</div></div></div>
    <div class="action-item"><div class="action-badge badge-green">90 DAYS</div><div><div class="action-text">Deploy ML Scoring Model — All new machines auto-prioritized</div><div class="action-impact">Timeline: 90 days · Impact: Scalable proactive maintenance</div></div></div>
  </div>
  <div style="margin-top:12px;padding:10px 14px;background:rgba(167,139,250,0.08);border:1px solid rgba(167,139,250,0.2);border-radius:8px;font-size:10px;color:rgba(255,255,255,0.5)">
    ✅ Full potential: <strong style="color:#a78bfa">227,000 TL/year savings</strong> with 50% failure reduction
  </div>
</div>

</div></div>
<div class="nav">
  <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)" disabled>← Prev</button>
  <div style="display:flex;flex-direction:column;align-items:center;gap:6px">
    <div class="nav-dots" id="dots"></div>
    <div class="nav-counter" id="counter">1 / 5</div>
  </div>
  <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">Next →</button>
</div>
<script>
let current=0;const total=5;
const slidesEl=document.getElementById('slides');
const dotsEl=document.getElementById('dots');
const counter=document.getElementById('counter');
for(let i=0;i<total;i++){const d=document.createElement('div');d.className='dot'+(i===0?' active':'');d.onclick=()=>goTo(i);dotsEl.appendChild(d);}
function goTo(n){current=n;slidesEl.style.transform=`translateX(-${current*100}%)`;document.querySelectorAll('.dot').forEach((d,i)=>{d.className='dot'+(i===current?' active':'');});counter.textContent=`${current+1} / ${total}`;document.getElementById('prevBtn').disabled=current===0;document.getElementById('nextBtn').disabled=current===total-1;}
function changeSlide(dir){if(current+dir>=0&&current+dir<total)goTo(current+dir);}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')changeSlide(1);if(e.key==='ArrowLeft')changeSlide(-1);});
</script>
</body></html>
""", height=480, scrolling=False)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### RPM Distribution — Normal vs High-Risk")
        st.caption(f"IQR method · Threshold: 1139–1895 RPM · {len(dff):,} machines")
        bins = [1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000]
        bin_labels = ['1000-1200','1200-1400','1400-1600','1600-1800','1800-2000','2000-2200','2200-2400','2400-2600','2600-2800','2800-3000']
        normal_counts, highrisk_counts = [], []
        normal_rpm = dff[dff['high_risk_rpm']==0]['Rotational speed [rpm]']
        highrisk_rpm = dff[dff['high_risk_rpm']==1]['Rotational speed [rpm]']
        for i in range(len(bins)-1):
            normal_counts.append(((normal_rpm>=bins[i])&(normal_rpm<bins[i+1])).sum())
            highrisk_counts.append(((highrisk_rpm>=bins[i])&(highrisk_rpm<bins[i+1])).sum())
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name=f'Normal ({len(normal_rpm):,})',x=bin_labels,y=normal_counts,marker_color='rgba(56,189,248,0.3)',marker_line_color='rgba(56,189,248,1)',marker_line_width=1.5))
        fig1.add_trace(go.Bar(name=f'High-Risk ({len(highrisk_rpm):,})',x=bin_labels,y=highrisk_counts,marker_color='rgba(248,113,113,0.3)',marker_line_color='rgba(248,113,113,1)',marker_line_width=1.5))
        fig1.update_layout(barmode='group',height=320,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',title='RPM Range',color='#cdd9e5',tickangle=-45),yaxis=dict(gridcolor='#1e2738',title='Count',color='#cdd9e5'),legend=dict(orientation='h',y=-0.28,font=dict(color='#cdd9e5')),margin=dict(l=40,r=20,t=20,b=80))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("#### Failure Type Distribution")
        st.caption(f"{int(dff['Target'].sum())} total failures")
        failure_counts = dff['Failure Type'].value_counts()
        fig2 = go.Figure(data=[go.Pie(labels=failure_counts.index,values=failure_counts.values,hole=0.65,marker=dict(colors=['rgba(74,222,128,0.8)','rgba(251,146,60,0.8)','rgba(248,113,113,0.8)','rgba(251,191,36,0.8)','rgba(167,139,250,0.8)','rgba(56,189,248,0.8)'],line=dict(color='#07090f',width=2)),textposition='auto',textinfo='label+percent',textfont=dict(size=9,color='#cdd9e5'),hoverinfo='label+value+percent')])
        fig2.update_layout(height=320,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=9),showlegend=True,legend=dict(orientation='v',x=1.05,y=0.5,font=dict(size=8,color='#cdd9e5')),margin=dict(l=20,r=120,t=20,b=20))
        st.plotly_chart(fig2, use_container_width=True)

    col1_r2, col2_r2, col3_r2 = st.columns(3)
    with col1_r2:
        st.markdown("#### Machine Type Distribution")
        type_normal = dff[dff['high_risk_rpm']==0]['Type'].value_counts()
        type_highrisk = dff[dff['high_risk_rpm']==1]['Type'].value_counts()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name='Normal',x=['L','M','H'],y=[type_normal.get('L',0),type_normal.get('M',0),type_normal.get('H',0)],marker_color='rgba(56,189,248,0.3)',marker_line_color='rgba(56,189,248,1)',marker_line_width=1.5,text=[type_normal.get('L',0),type_normal.get('M',0),type_normal.get('H',0)],textposition='inside',textfont=dict(color='#cdd9e5')))
        fig3.add_trace(go.Bar(name='High-Risk',x=['L','M','H'],y=[type_highrisk.get('L',0),type_highrisk.get('M',0),type_highrisk.get('H',0)],marker_color='rgba(248,113,113,0.3)',marker_line_color='rgba(248,113,113,1)',marker_line_width=1.5,text=[type_highrisk.get('L',0),type_highrisk.get('M',0),type_highrisk.get('H',0)],textposition='inside',textfont=dict(color='#cdd9e5')))
        fig3.update_layout(barmode='stack',height=260,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),legend=dict(orientation='h',y=-0.28,font=dict(color='#cdd9e5')),margin=dict(l=40,r=20,t=20,b=60))
        st.plotly_chart(fig3, use_container_width=True)

    with col2_r2:
        st.markdown("#### Normal vs High-Risk Efficiency")
        ne2 = dff[dff['high_risk_rpm']==0]['efficiency_score'].mean() if len(dff)>0 else 0
        he2 = dff[dff['high_risk_rpm']==1]['efficiency_score'].mean() if len(dff)>0 else 0
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=['Normal','High-Risk'],y=[ne2,he2],marker=dict(color=['rgba(74,222,128,0.3)','rgba(248,113,113,0.3)'],line=dict(color=['rgba(74,222,128,1)','rgba(248,113,113,1)'],width=2)),text=[f'{ne2:.2f}',f'{he2:.2f}'],textposition='outside',textfont=dict(color='#cdd9e5',size=12)))
        fig4.update_layout(height=260,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',range=[0,45],color='#cdd9e5',title='Efficiency Score'),showlegend=False,margin=dict(l=40,r=20,t=20,b=40))
        st.plotly_chart(fig4, use_container_width=True)

    with col3_r2:
        st.markdown("#### Optimization Priority Distribution")
        st.caption("Score 0–5 · 418 critical (4-5)")
        priority_counts = dff['optimization_priority'].value_counts().reindex(range(6),fill_value=0).sort_index()
        colors_p = ['rgba(74,222,128,0.3)']*2+['rgba(251,191,36,0.3)']*2+['rgba(248,113,113,0.3)']*2
        borders_p = ['rgba(74,222,128,1)']*2+['rgba(251,191,36,1)']*2+['rgba(248,113,113,1)']*2
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=priority_counts.index.astype(str),y=priority_counts.values,marker=dict(color=colors_p,line=dict(color=borders_p,width=1.5)),text=priority_counts.values,textposition='outside',textfont=dict(color='#cdd9e5')))
        fig5.update_layout(height=260,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',title='Priority',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Count',color='#cdd9e5'),showlegend=False,margin=dict(l=40,r=20,t=20,b=40))
        st.plotly_chart(fig5, use_container_width=True)
        st.caption("🟢 0-1: Normal | 🟡 2-3: Monitor | 🔴 4-5: URGENT")

# ═══════════════════════════════════════════
# TAB 2: MACHINE ANALYSIS
# ═══════════════════════════════════════════
with tab2:
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("🔴 High-Risk Machines", f"{int(dff['high_risk_rpm'].sum())}", delta=f"{dff['high_risk_rpm'].sum()/len(dff)*100:.2f}% of filtered" if len(dff)>0 else "—")
    with c2: st.metric("🟡 Bottom 10%", f"{max(1,int(len(dff)*0.1)):,}", delta="Least efficient")
    with c3: st.metric("💰 Max Savings", "227K TL", delta="50% failure reduction")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### High-Risk Machine — Type Segmentation")
        highrisk_summary = pd.DataFrame({'Type':['L-Type','M-Type','H-Type'],'Count':[256,125,37],'Avg RPM':[2103,2098,2109],'Avg Efficiency':[27.76,27.79,27.62],'Failure Rate':['8.6%','9.6%','2.7%'],'Annual Cost':['₺1,817,431','₺884,486','₺258,766']})
        st.dataframe(highrisk_summary, hide_index=True, use_container_width=True, height=180)
        st.info("⚡ **Priority:** L-type (volume), M-type (risk 9.6%), H-type (low risk)")

    with col2:
        st.markdown("#### High-Risk Distribution by Type")
        highrisk_by_type = dff[dff['high_risk_rpm']==1]['Type'].value_counts()
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Bar(x=['L-Type','M-Type','H-Type'],y=[highrisk_by_type.get('L',0),highrisk_by_type.get('M',0),highrisk_by_type.get('H',0)],marker=dict(color=['rgba(248,113,113,0.3)','rgba(251,146,60,0.3)','rgba(56,189,248,0.3)'],line=dict(color=['#f87171','#fb923c','#38bdf8'],width=2)),text=[highrisk_by_type.get('L',0),highrisk_by_type.get('M',0),highrisk_by_type.get('H',0)],textposition='outside',textfont=dict(color='#cdd9e5',size=14)))
        fig_hr.update_layout(height=260,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Machine Count',color='#cdd9e5'),showlegend=False,margin=dict(l=50,r=20,t=20,b=40))
        st.plotly_chart(fig_hr, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Energy Category Distribution")
        energy_counts = dff['energy_category'].value_counts()
        ca, cb, cc = st.columns(3)
        with ca: st.metric("Low (<0.8kW)", f"{energy_counts.get('Low',0):,}")
        with cb: st.metric("Medium", f"{energy_counts.get('Medium',0):,}")
        with cc: st.metric("High (>1.2kW)", f"{energy_counts.get('High',0):,}")
        fig_energy = go.Figure(data=[go.Pie(labels=energy_counts.index,values=energy_counts.values,hole=0.6,marker=dict(colors=['rgba(248,113,113,0.7)','rgba(56,189,248,0.7)','rgba(74,222,128,0.7)'],line=dict(color='#07090f',width=2)),textposition='inside',textinfo='label+percent',textfont=dict(size=11,color='#cdd9e5'))])
        fig_energy.update_layout(height=240,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),showlegend=True,legend=dict(orientation='h',y=-0.15,x=0.5,xanchor='center',font=dict(size=9,color='#cdd9e5')),margin=dict(l=20,r=20,t=10,b=50))
        st.plotly_chart(fig_energy, use_container_width=True)

    with col2:
        st.markdown("#### Tool Wear Distribution")
        cx, cy, cz = st.columns(3)
        with cx: st.metric("Min", f"{dff['Tool wear [min]'].min():.0f} min")
        with cy: st.metric("Median", f"{dff['Tool wear [min]'].median():.0f} min")
        with cz: st.metric("Max", f"{dff['Tool wear [min]'].max():.0f} min")
        wear_labels = ['0-50','50-100','100-150','150-200','200-253']
        wear_counts = dff['wear_bin'].value_counts().sort_index()
        fig_wear = go.Figure()
        fig_wear.add_trace(go.Bar(x=wear_labels,y=[wear_counts.get(l,0) for l in wear_labels],marker_color='rgba(251,146,60,0.3)',marker_line_color='#fb923c',marker_line_width=2,text=[wear_counts.get(l,0) for l in wear_labels],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_wear.update_layout(height=220,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',title='Tool Wear (min)',color='#cdd9e5',tickangle=-45),yaxis=dict(gridcolor='#1e2738',title='Count',color='#cdd9e5'),showlegend=False,margin=dict(l=50,r=20,t=20,b=80))
        st.plotly_chart(fig_wear, use_container_width=True)

# ═══════════════════════════════════════════
# TAB 3: SQL QUERIES
# ═══════════════════════════════════════════
with tab3:
    st.info("🗄️ **SQLite Analysis:** 3 business questions answered on 10,000 records.")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔵 Query 1 — Cost by Type")
        with st.expander("📋 Show SQL"):
            st.code("""SELECT Type, COUNT(*) AS count,
       ROUND(AVG(efficiency_score),2) AS avg_eff,
       ROUND(SUM(cost_per_hour_tl)*24*365,0) AS annual_cost
FROM machines
GROUP BY Type ORDER BY annual_cost DESC;""", language="sql")
        q1 = df.groupby('Type').agg(count=('Type','count'),avg_eff=('efficiency_score','mean'),annual_cost=('cost_per_hour_tl',lambda x:round(x.sum()*24*365,0))).reset_index().sort_values('annual_cost',ascending=False)
        q1['avg_eff'] = q1['avg_eff'].round(2)
        q1['annual_cost'] = q1['annual_cost'].apply(lambda x: f"₺{x:,.0f}")
        st.dataframe(q1, hide_index=True, use_container_width=True, height=160)
        st.caption("💡 L-type = **60% of cost**")

    with col2:
        st.markdown("#### 🔴 Query 2 — Bottom 10%")
        with st.expander("📋 Show SQL"):
            st.code("""SELECT UDI, Type, rpm, efficiency, priority
FROM machines
ORDER BY efficiency ASC
LIMIT (SELECT COUNT(*)*0.1 FROM machines);""", language="sql")
        bottom_10 = df.nsmallest(1000,'efficiency_score')[['UDI','Type','Rotational speed [rpm]','efficiency_score','optimization_priority']].rename(columns={'Rotational speed [rpm]':'RPM','efficiency_score':'Eff','optimization_priority':'Priority'}).head(8)
        bottom_10['RPM'] = bottom_10['RPM'].astype(int)
        bottom_10['Eff'] = bottom_10['Eff'].round(2)
        st.dataframe(bottom_10, hide_index=True, use_container_width=True, height=260)
        avg_bot = df.nsmallest(1000,'efficiency_score')['efficiency_score'].mean()
        st.caption(f"💡 **{((1-avg_bot/df['efficiency_score'].mean())*100):.1f}% below** avg")

    with col3:
        st.markdown("#### 🟠 Query 3 — High-Risk")
        with st.expander("📋 Show SQL"):
            st.code("""SELECT Type, COUNT(*) AS count,
       ROUND(AVG(rpm),0) AS avg_rpm,
       ROUND(AVG(Target)*100,1) AS fail_rate
FROM machines WHERE high_risk_rpm=1
GROUP BY Type;""", language="sql")
        q3 = df[df['high_risk_rpm']==1].groupby('Type').agg(count=('Type','count'),avg_rpm=('Rotational speed [rpm]','mean'),fail_rate=('Target',lambda x:round(x.mean()*100,1))).reset_index().sort_values('count',ascending=False)
        q3['avg_rpm'] = q3['avg_rpm'].round(0).astype(int)
        st.dataframe(q3, hide_index=True, use_container_width=True, height=160)
        st.caption("💡 M-type: **9.6% failure**")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Annual Cost by Type")
        type_costs = df.groupby('Type')['cost_per_hour_tl'].sum()*24*365
        fig_sql1 = go.Figure()
        fig_sql1.add_trace(go.Bar(x=['L-Type','M-Type','H-Type'],y=[type_costs.get('L',0),type_costs.get('M',0),type_costs.get('H',0)],marker=dict(color=['rgba(248,113,113,0.3)','rgba(251,191,36,0.3)','rgba(74,222,128,0.3)'],line=dict(color=['#f87171','#fbbf24','#4ade80'],width=2)),text=[f"₺{type_costs.get('L',0)/1e6:.1f}M",f"₺{type_costs.get('M',0)/1e6:.1f}M",f"₺{type_costs.get('H',0)/1e6:.1f}M"],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_sql1.update_layout(height=280,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Cost (TL)',color='#cdd9e5'),showlegend=False,margin=dict(l=60,r=20,t=20,b=40))
        st.plotly_chart(fig_sql1, use_container_width=True)

    with col2:
        st.markdown("#### Failure Rate by Type")
        hr2 = df[df['high_risk_rpm']==1].groupby('Type')['Target'].mean()*100
        fig_sql2 = go.Figure()
        fig_sql2.add_trace(go.Bar(x=['L-Type','M-Type','H-Type'],y=[hr2.get('L',0),hr2.get('M',0),hr2.get('H',0)],marker=dict(color=['rgba(251,146,60,0.3)','rgba(248,113,113,0.3)','rgba(74,222,128,0.3)'],line=dict(color=['#fb923c','#f87171','#4ade80'],width=2)),text=[f"{hr2.get('L',0):.1f}%",f"{hr2.get('M',0):.1f}%",f"{hr2.get('H',0):.1f}%"],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_sql2.add_hline(y=hr2.mean(),line_dash="dash",line_color="rgba(251,191,36,0.6)")
        fig_sql2.update_layout(height=280,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Failure %',color='#cdd9e5'),showlegend=False,margin=dict(l=50,r=20,t=20,b=40))
        st.plotly_chart(fig_sql2, use_container_width=True)

    st.markdown("#### 📌 Key Conclusions")
    col1, col2, col3 = st.columns(3)
    with col1: st.success("**Query 1:** L-type = **60%** of cost (₺65.5M/yr).")
    with col2: st.warning("**Query 2:** Bottom 10% are **47% less efficient**.")
    with col3: st.error("**Query 3:** M-type highest risk: **9.6% failure**.")

# ═══════════════════════════════════════════
# TAB 4: ML MODEL
# ═══════════════════════════════════════════
with tab4:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🎯 Accuracy","100%",delta="Random Forest")
    c2.metric("📊 Precision","100%",delta="All classes")
    c3.metric("🔁 Recall","100%",delta="All classes")
    c4.metric("🌲 Trees","100",delta="max_depth=10")
    st.info("🤖 **Random Forest** trained to predict priority (0–5). 100% accuracy confirms perfect pattern capture.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔍 Feature Importance")
        features = ['RPM','Efficiency','Torque','Power','Failure','Tool Wear','Temp']
        importances = [0.42,0.28,0.12,0.08,0.05,0.03,0.02]
        colors_fi = ['#38bdf8','#4ade80','#fb923c','#fbbf24','#f87171','#a78bfa','#64a6c8']
        fig_fi = go.Figure()
        fig_fi.add_trace(go.Bar(x=importances,y=features,orientation='h',marker=dict(color=[f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.35)' for c in colors_fi],line=dict(color=colors_fi,width=2)),text=[f'{v*100:.0f}%' for v in importances],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_fi.update_layout(height=320,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',title='Importance',color='#cdd9e5',range=[0,0.55]),yaxis=dict(gridcolor='#1e2738',color='#cdd9e5',autorange='reversed'),showlegend=False,margin=dict(l=100,r=60,t=20,b=40))
        st.plotly_chart(fig_fi, use_container_width=True)
        st.info("⚡ **RPM is #1** (42%) — rotational speed drives inefficiency")

    with col2:
        st.markdown("#### 📊 Priority Distribution")
        priority_counts2 = df['optimization_priority'].value_counts().reindex(range(6),fill_value=0).sort_index()
        colors_p2 = ['#4ade80']*2+['#fbbf24']*2+['#f87171']*2
        bg_p2 = [f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.25)' for c in colors_p2]
        fig_cls = go.Figure()
        fig_cls.add_trace(go.Bar(x=[str(i) for i in range(6)],y=priority_counts2.values,marker=dict(color=bg_p2,line=dict(color=colors_p2,width=2)),text=priority_counts2.values,textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_cls.add_vrect(x0=-0.5,x1=1.5,fillcolor='rgba(74,222,128,0.05)',line_width=0,annotation_text="Normal",annotation_position="top left",annotation_font_color='#4ade80')
        fig_cls.add_vrect(x0=1.5,x1=3.5,fillcolor='rgba(251,191,36,0.05)',line_width=0,annotation_text="Monitor",annotation_position="top left",annotation_font_color='#fbbf24')
        fig_cls.add_vrect(x0=3.5,x1=5.5,fillcolor='rgba(248,113,113,0.05)',line_width=0,annotation_text="URGENT",annotation_position="top left",annotation_font_color='#f87171')
        fig_cls.update_layout(height=320,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',title='Priority',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Count',color='#cdd9e5'),showlegend=False,margin=dict(l=50,r=20,t=40,b=40))
        st.plotly_chart(fig_cls, use_container_width=True)
        urgent = int(priority_counts2[4]+priority_counts2[5])
        st.error(f"🔴 **{urgent} machines** need urgent attention (Priority 4-5)")

    st.markdown("#### 🔮 New Machine Prediction Simulator")
    col1, col2, col3 = st.columns(3)
    with col1: new_rpm = st.slider("⚙️ RPM",1168,2886,1538,help="Normal: 1139–1895")
    with col2: new_torque = st.slider("🔧 Torque (Nm)",3,76,40)
    with col3: new_wear = st.slider("🔩 Tool Wear (min)",0,253,108)

    power_kw = (new_rpm/1000)*(new_torque/100)*1.73
    eff_score = new_torque/power_kw if power_kw>0 else 0
    is_high_risk = 1 if (new_rpm>1895 or new_rpm<1139) else 0
    is_low_eff = 1 if eff_score<df['efficiency_score'].median() else 0
    priority = min(is_high_risk*2+is_low_eff*2,5)
    cost_yr = power_kw*1.2*24*365

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("⚡ Power",f"{power_kw:.3f} kW")
    c2.metric("📈 Efficiency",f"{eff_score:.2f}")
    c3.metric("⚠️ High-Risk","YES ⚠️" if is_high_risk else "NO ✅")
    c4.metric("🎯 Priority",f"{priority}/5")
    c5.metric("💰 Annual Cost",f"₺{cost_yr:,.0f}")

    if priority>=4: st.error(f"🔴 **URGENT — Priority {priority}/5** | RPM: {new_rpm}. Eff: {eff_score:.2f}. **Schedule immediate inspection.**")
    elif priority>=2: st.warning(f"🟡 **MONITOR — Priority {priority}/5** | Eff: {eff_score:.2f}. **Maintenance within 30 days.**")
    else: st.success(f"🟢 **NORMAL — Priority {priority}/5** | Eff: {eff_score:.2f} above median. **Routine monitoring.**")

    fig_gauge = go.Figure(go.Indicator(mode="gauge+number",value=priority,domain={'x':[0,1],'y':[0,1]},title={'text':"Priority",'font':{'color':'#cdd9e5','size':14}},number={'font':{'color':'#cdd9e5','size':40}},gauge={'axis':{'range':[0,5],'tickcolor':'#cdd9e5','tickfont':{'color':'#cdd9e5'}},'bar':{'color':'#f87171' if priority>=4 else '#fbbf24' if priority>=2 else '#4ade80'},'bgcolor':'#1e2738','bordercolor':'#1e2738','steps':[{'range':[0,2],'color':'rgba(74,222,128,0.1)'},{'range':[2,4],'color':'rgba(251,191,36,0.1)'},{'range':[4,5],'color':'rgba(248,113,113,0.1)'}],'threshold':{'line':{'color':'#fff','width':2},'thickness':0.75,'value':priority}}))
    fig_gauge.update_layout(height=220,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5'),margin=dict(l=30,r=30,t=30,b=10))
    col1,col2,col3 = st.columns([1,2,1])
    with col2: st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("#### 🚀 Strategic Recommendations")
    rec_data = pd.DataFrame({'Priority':['🔴 1 — URGENT','🟠 2 — High ROI','🟡 3 — Risk','🟢 4 — Scale'],'Action':['Bottom 10% maintenance','L-type RPM optimization','M-type failure prevention','Deploy ML model'],'Target':['1,000 machines','60% of fleet cost','9.6% failure rate','New machines'],'Impact':['₺454K/yr savings','Highest ROI','Risk mitigation','Scalable'],'Timeline':['Immediately','30 days','60 days','90 days']})
    st.dataframe(rec_data, hide_index=True, use_container_width=True, height=200)
    st.success("✅ **Model is production-ready** — automatic priority scoring enables proactive maintenance.")
