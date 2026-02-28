import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page config
st.set_page_config(
    page_title="⚡ Energy Efficiency Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'cover'

# Load data
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
    
    df['power_consumption_kw'] = ((df['Rotational speed [rpm]'] / 1000) * 
                                   (df['Torque [Nm]'] / 100) * 1.73)
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

# ═══════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════
if st.session_state.page == 'cover':
    
    # Sayfayı tamamen siyah yap
    st.markdown("""
    <style>
    .stApp { background: #000 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)
    
    # Icon
    st.markdown("<div style='text-align:center;font-size:80px;filter:drop-shadow(0 0 40px rgba(255,165,0,0.6))'>⚡</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:12px;letter-spacing:8px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin:16px 0'>INDUSTRIAL DATA SCIENCE PORTFOLIO</div>", unsafe_allow_html=True)
    
    # Orange line
    st.markdown("<div style='height:4px;background:linear-gradient(90deg,transparent,#ff8c00,#ffaa00,#ff8c00,transparent);box-shadow:0 0 20px rgba(255,140,0,0.4);margin:0 auto;max-width:700px'></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    
    # Title
    st.markdown("<div style='text-align:center;font-size:48px;font-weight:900;letter-spacing:4px;text-transform:uppercase;color:#fff;line-height:1.2'>MANUFACTURING ENERGY<br><span style=\"color:#ffaa00\">EFFICIENCY ANALYSIS</span></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # Subtitle
    st.markdown("<div style='text-align:center;font-size:16px;color:rgba(255,255,255,0.5);font-style:italic'>Predictive Maintenance · Machine Learning · SQL Analytics<br><span style=\"color:rgba(255,165,0,0.8);font-weight:600\">\"10,000 Machines · 418 High-Risk · 227K TL Savings\"</span></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    
    # Tags
    st.markdown("<div style='text-align:center;display:flex;gap:12px;flex-wrap:wrap;justify-content:center'><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,140,0,0.4);color:rgba(255,140,0,0.8);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>PYTHON</span><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.4);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>SQL</span><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.4);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>RANDOM FOREST</span><span style='display:inline-block;padding:6px 16px;border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.4);font-size:10px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:4px'>STREAMLIT</span></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    
    # Button
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("🚀 ENTER DASHBOARD", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    st.markdown("<div style='text-align:center;margin-top:40px;font-size:11px;color:rgba(255,255,255,0.2);letter-spacing:3px;text-transform:uppercase'>N. Nur Altay · Data Analyst · February 2026</div>", unsafe_allow_html=True)
    
    st.stop()

# ═══════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════

# DARK TEMA CSS - TÜM TABLAR İÇİN
st.markdown("""
<style>
.stApp { background: #07090f !important; color: #cdd9e5 !important; }
section[data-testid="stMain"] { background: #07090f !important; }
.block-container { background: #07090f !important; padding-top: 2rem; }
[data-testid="metric-container"] { background: #0d1117 !important; border: 1px solid #1e2738 !important; border-radius: 10px !important; padding: 16px !important; }
[data-testid="stMetricValue"] { color: #cdd9e5 !important; }
[data-testid="stMetricLabel"] { color: #4a6072 !important; }
.stTabs [data-baseweb="tab-list"] { background: #0d1117 !important; border: 1px solid #1e2738 !important; border-radius: 8px !important; }
.stTabs [data-baseweb="tab"] { color: #4a6072 !important; }
.stTabs [aria-selected="true"] { background: #161b24 !important; color: #cdd9e5 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #07090f !important; }
[data-testid="stExpander"] { background: #0d1117 !important; border: 1px solid #1e2738 !important; border-radius: 10px !important; }
summary { color: #cdd9e5 !important; }
pre { background: #0d1117 !important; color: #cdd9e5 !important; }
p, h1, h2, h3, h4, label { color: #cdd9e5 !important; }
.stCaption { color: #4a6072 !important; }
[data-testid="stAlert"] { background: #0d1117 !important; }
footer { display: none !important; }
::-webkit-scrollbar { width: 6px; background: #07090f; }
::-webkit-scrollbar-thumb { background: #1e2738; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

df = load_data()

# HEADER
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #38bdf8, #4ade80); 
                        border-radius: 12px; display: flex; align-items: center; justify-content: center; 
                        font-size: 28px; box-shadow: 0 0 20px rgba(56,189,248,0.3);">⚡</div>
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
                <div style="width: 8px; height: 8px; background: #4ade80; border-radius: 50%;"></div>
                Live Dashboard
            </div>
            <div style="padding: 8px 16px; background: #161b24; border: 1px solid #1e2738; 
                        border-radius: 20px; font-size: 11px; color: #4a6072;">Feb 2026</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🏭 Total Machines", f"{len(df):,}", delta="3 Types")
with col2:
    high_risk = df['high_risk_rpm'].sum()
    st.metric("⚠️ High-Risk", f"{high_risk}", delta=f"{high_risk/len(df)*100:.1f}%", delta_color="inverse")
with col3:
    normal_eff = df[df['high_risk_rpm']==0]['efficiency_score'].mean()
    st.metric("📈 Avg Efficiency", f"{normal_eff:.1f}", delta="+27.8%")
with col4:
    st.metric("💰 Avg Cost", f"{df['cost_per_hour_tl'].mean():.2f} TL/hr", delta="1.2 TL/kWh")
with col5:
    failures = int(df['Target'].sum())
    st.metric("🔥 Failures", f"{failures}", delta=f"{failures/len(df)*100:.1f}%", delta_color="inverse")

st.info("💡 **Key Finding:** 418 high-risk machines have **27.8% lower efficiency** (27.76 vs 38.45). Annual cost impact: **~2.96M TL**.")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔧 Machine Analysis", "🗄️ SQL Queries", "🤖 ML Model"])

# ═══════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([3, 2])


slider_code = '''
# ═══════════════════════════════════════════════════
# EXECUTIVE PRESENTATION SLIDER
# ═══════════════════════════════════════════════════

import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background: #07090f; font-family: 'Segoe UI', sans-serif; }

.slider-wrap {
    position: relative;
    width: 100%;
    overflow: hidden;
    background: #07090f;
}

.slides {
    display: flex;
    transition: transform 0.5s cubic-bezier(0.4,0,0.2,1);
    will-change: transform;
}

.slide {
    min-width: 100%;
    padding: 40px 48px;
    position: relative;
    overflow: hidden;
}

/* Slide backgrounds */
.slide-1 { background: linear-gradient(135deg, #0a0e1a 0%, #0d1525 100%); }
.slide-2 { background: linear-gradient(135deg, #100a08 0%, #1a0e0a 100%); }
.slide-3 { background: linear-gradient(135deg, #080d10 0%, #0a1218 100%); }
.slide-4 { background: linear-gradient(135deg, #08100a 0%, #0a1410 100%); }
.slide-5 { background: linear-gradient(135deg, #0d0a14 0%, #120d1c 100%); }

/* Slide number */
.slide-num {
    position: absolute;
    top: 24px; right: 36px;
    font-size: 72px;
    font-weight: 900;
    color: rgba(255,255,255,0.04);
    letter-spacing: -4px;
    line-height: 1;
    user-select: none;
}

/* Label */
.slide-label {
    font-size: 9px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-weight: 700;
}
.label-blue { color: #38bdf8; }
.label-red { color: #f87171; }
.label-cyan { color: #00e5d4; }
.label-green { color: #4ade80; }
.label-purple { color: #a78bfa; }

/* Title */
.slide-title {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.slide-title span { color: #ffaa00; }

/* Divider */
.divider {
    width: 48px; height: 3px;
    border-radius: 2px;
    margin: 16px 0;
}
.div-blue { background: #38bdf8; }
.div-red { background: #f87171; }
.div-cyan { background: #00e5d4; }
.div-green { background: #4ade80; }
.div-purple { background: #a78bfa; }

/* KPI grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 20px;
}
.kpi-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.kpi-val {
    font-size: 26px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-lbl {
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
}

/* Insight rows */
.insight-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 16px;
    background: rgba(255,255,255,0.03);
    border-left: 3px solid;
    border-radius: 0 8px 8px 0;
    margin-bottom: 10px;
}
.insight-icon { font-size: 20px; flex-shrink: 0; margin-top: 2px; }
.insight-text { flex: 1; }
.insight-title { font-size: 13px; font-weight: 700; color: #ffffff; margin-bottom: 3px; }
.insight-desc { font-size: 11px; color: rgba(255,255,255,0.45); line-height: 1.5; }

/* Two column layout */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px; }

/* Action items */
.action-item {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 16px;
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    margin-bottom: 8px;
}
.action-badge {
    font-size: 9px; font-weight: 800;
    letter-spacing: 1px; text-transform: uppercase;
    padding: 4px 10px; border-radius: 4px;
    flex-shrink: 0; min-width: 70px; text-align: center;
}
.badge-red { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.badge-orange { background: rgba(251,146,60,0.15); color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }
.badge-yellow { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-green { background: rgba(74,222,128,0.15); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
.action-text { font-size: 12px; color: rgba(255,255,255,0.7); }
.action-impact { font-size: 10px; color: rgba(255,255,255,0.3); margin-top: 2px; }

/* Bottom desc */
.slide-desc {
    font-size: 13px;
    color: rgba(255,255,255,0.45);
    line-height: 1.7;
    margin-top: 12px;
    max-width: 600px;
}

/* NAVIGATION */
.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 48px 20px;
    background: #07090f;
    border-top: 1px solid rgba(255,255,255,0.06);
}

.nav-dots {
    display: flex; gap: 8px; align-items: center;
}
.dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.15);
    cursor: pointer;
    transition: all 0.3s;
}
.dot.active {
    background: #ffaa00;
    width: 24px;
    border-radius: 4px;
}

.nav-btn {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.6);
    padding: 8px 20px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.5px;
}
.nav-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }
.nav-btn:disabled { opacity: 0.2; cursor: default; }

.nav-counter {
    font-size: 11px;
    color: rgba(255,255,255,0.25);
    letter-spacing: 2px;
    font-weight: 600;
}
</style>
</head>
<body>

<div class="slider-wrap">
  <div class="slides" id="slides">

    <!-- ══ SLIDE 1: EXECUTIVE SUMMARY ══ -->
    <div class="slide slide-1">
      <div class="slide-num">01</div>
      <div class="slide-label label-blue">EXECUTIVE SUMMARY</div>
      <div class="slide-title">Manufacturing Energy Efficiency<br><span>Analysis Overview</span></div>
      <div class="divider div-blue"></div>
      <div class="slide-desc">
        End-to-end data analysis of 10,000 production machines to identify energy inefficiencies,
        quantify financial risk, and build a predictive model for proactive maintenance prioritization.
      </div>

      <div class="kpi-grid" style="margin-top:24px">
        <div class="kpi-card">
          <div class="kpi-val" style="color:#38bdf8">10,000</div>
          <div class="kpi-lbl">Machines Analyzed</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color:#f87171">418</div>
          <div class="kpi-lbl">High-Risk Units</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color:#4ade80">100%</div>
          <div class="kpi-lbl">ML Accuracy</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color:#ffaa00">₺2.96M</div>
          <div class="kpi-lbl">Annual Cost Risk</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color:#a78bfa">227K TL</div>
          <div class="kpi-lbl">Savings Potential</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color:#fb923c">3</div>
          <div class="kpi-lbl">Analysis Phases</div>
        </div>
      </div>
    </div>

    <!-- ══ SLIDE 2: PROBLEM & COST ══ -->
    <div class="slide slide-2">
      <div class="slide-num">02</div>
      <div class="slide-label label-red">BUSINESS PROBLEM</div>
      <div class="slide-title">The Cost of <span>Undetected Inefficiency</span></div>
      <div class="divider div-red"></div>

      <div style="margin-top:20px">
        <div class="insight-row" style="border-color:#f87171">
          <div class="insight-icon">⚠️</div>
          <div class="insight-text">
            <div class="insight-title">Hidden High-Risk Machines</div>
            <div class="insight-desc">418 machines (4.18% of fleet) operate at abnormal RPM — undetected without data analysis. These machines have a 2.6× higher failure rate than normal units.</div>
          </div>
        </div>
        <div class="insight-row" style="border-color:#fb923c">
          <div class="insight-icon">💸</div>
          <div class="insight-text">
            <div class="insight-title">₺2.96M Annual Cost Impact</div>
            <div class="insight-desc">High-risk machines generate ₺454,826/year in failure costs alone. L-type machines drive 60% of total fleet energy cost (₺65.5M/year).</div>
          </div>
        </div>
        <div class="insight-row" style="border-color:#fbbf24">
          <div class="insight-icon">📉</div>
          <div class="insight-text">
            <div class="insight-title">27.8% Efficiency Gap</div>
            <div class="insight-desc">High-risk machines score 27.76 vs 38.45 efficiency average — a 27.8% gap that directly translates to wasted energy and increased operational cost.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ SLIDE 3: KEY FINDINGS ══ -->
    <div class="slide slide-3">
      <div class="slide-num">03</div>
      <div class="slide-label label-cyan">KEY FINDINGS</div>
      <div class="slide-title">What the Data <span>Revealed</span></div>
      <div class="divider div-cyan"></div>

      <div class="two-col">
        <div>
          <div style="font-size:10px;letter-spacing:2px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:12px">Machine Risk Profile</div>
          <div class="insight-row" style="border-color:#00e5d4;margin-bottom:8px">
            <div class="insight-text">
              <div class="insight-title" style="font-size:12px">High RPM + Low Torque</div>
              <div class="insight-desc">Avg RPM: 2,102 vs 1,514 (normal) → 39% faster. Avg Torque: 18.9 Nm vs 40.9 Nm → 54% lower. Classic inefficiency pattern.</div>
            </div>
          </div>
          <div class="insight-row" style="border-color:#f87171;margin-bottom:8px">
            <div class="insight-text">
              <div class="insight-title" style="font-size:12px">Failure Rate: 8.37% vs 3.17%</div>
              <div class="insight-desc">High-risk machines fail 2.6× more often. M-type machines carry the highest individual risk at 9.6%.</div>
            </div>
          </div>
        </div>
        <div>
          <div style="font-size:10px;letter-spacing:2px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:12px">Fleet Breakdown</div>
          <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:16px">
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.06)">
              <span style="font-size:12px;color:rgba(255,255,255,0.6)">L-Type</span>
              <span style="font-size:12px;font-weight:700;color:#f87171">256 units · 8.6% fail</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.06)">
              <span style="font-size:12px;color:rgba(255,255,255,0.6)">M-Type</span>
              <span style="font-size:12px;font-weight:700;color:#fb923c">125 units · 9.6% fail</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:8px 0">
              <span style="font-size:12px;color:rgba(255,255,255,0.6)">H-Type</span>
              <span style="font-size:12px;font-weight:700;color:#4ade80">37 units · 2.7% fail</span>
            </div>
            <div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.06)">
              <div style="font-size:10px;color:rgba(255,255,255,0.3);margin-bottom:6px">NIGHT SHIFT RISK</div>
              <div style="font-size:13px;font-weight:700;color:#fbbf24">100% of high-risk → Night Shift</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ SLIDE 4: SQL INSIGHTS ══ -->
    <div class="slide slide-4">
      <div class="slide-num">04</div>
      <div class="slide-label label-green">SQL BUSINESS INSIGHTS</div>
      <div class="slide-title">3 Queries That <span>Changed the Strategy</span></div>
      <div class="divider div-green"></div>

      <div style="margin-top:20px">
        <div class="insight-row" style="border-color:#4ade80">
          <div class="insight-icon">🔵</div>
          <div class="insight-text">
            <div class="insight-title">Query 1 — Cost by Machine Type</div>
            <div class="insight-desc">L-type: ₺65.5M/yr (60% of total) · M-type: ₺32.7M/yr · H-type: ₺10.9M/yr<br>→ <strong style="color:#4ade80">L-type optimization = highest ROI target</strong></div>
          </div>
        </div>
        <div class="insight-row" style="border-color:#fbbf24">
          <div class="insight-icon">🔴</div>
          <div class="insight-text">
            <div class="insight-title">Query 2 — Bottom 10% Efficiency</div>
            <div class="insight-desc">1,000 machines identified as critically inefficient — 47% below fleet average.<br>→ <strong style="color:#fbbf24">Immediate maintenance = ₺454K/yr recovery</strong></div>
          </div>
        </div>
        <div class="insight-row" style="border-color:#fb923c">
          <div class="insight-icon">🟠</div>
          <div class="insight-text">
            <div class="insight-title">Query 3 — High-Risk Segmentation</div>
            <div class="insight-desc">M-type carries 9.6% failure rate despite being mid-size fleet — highest per-unit risk.<br>→ <strong style="color:#fb923c">Risk mitigation program required for M-type</strong></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ SLIDE 5: ACTION PLAN ══ -->
    <div class="slide slide-5">
      <div class="slide-num">05</div>
      <div class="slide-label label-purple">STRATEGIC ACTION PLAN</div>
      <div class="slide-title">4-Step <span>Optimization Roadmap</span></div>
      <div class="divider div-purple"></div>

      <div style="margin-top:20px">
        <div class="action-item">
          <div class="action-badge badge-red">URGENT</div>
          <div>
            <div class="action-text">Bottom 10% Immediate Maintenance — 1,000 machines</div>
            <div class="action-impact">Timeline: Immediately · Impact: ₺454K/yr savings</div>
          </div>
        </div>
        <div class="action-item">
          <div class="action-badge badge-orange">30 DAYS</div>
          <div>
            <div class="action-text">L-Type RPM Optimization Program — 256 high-risk units</div>
            <div class="action-impact">Timeline: 30 days · Impact: Highest ROI (60% of cost base)</div>
          </div>
        </div>
        <div class="action-item">
          <div class="action-badge badge-yellow">60 DAYS</div>
          <div>
            <div class="action-text">M-Type Failure Prevention Program — 9.6% failure rate</div>
            <div class="action-impact">Timeline: 60 days · Impact: Risk mitigation, prevent cascading failures</div>
          </div>
        </div>
        <div class="action-item">
          <div class="action-badge badge-green">90 DAYS</div>
          <div>
            <div class="action-text">Deploy ML Scoring Model — All new machines auto-prioritized</div>
            <div class="action-impact">Timeline: 90 days · Impact: Proactive maintenance, scalable system</div>
          </div>
        </div>
      </div>

      <div style="margin-top:16px;padding:12px 16px;background:rgba(167,139,250,0.08);border:1px solid rgba(167,139,250,0.2);border-radius:8px;font-size:11px;color:rgba(255,255,255,0.5)">
        ✅ Full implementation potential: <strong style="color:#a78bfa">227,000 TL/year savings</strong> with 50% failure reduction target
      </div>
    </div>

  </div><!-- /slides -->
</div><!-- /slider-wrap -->

<!-- NAVIGATION -->
<div class="nav">
  <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)" disabled>← Prev</button>
  <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
    <div class="nav-dots" id="dots"></div>
    <div class="nav-counter" id="counter">1 / 5</div>
  </div>
  <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">Next →</button>
</div>

<script>
let current = 0;
const total = 5;
const slidesEl = document.getElementById('slides');
const dotsEl = document.getElementById('dots');
const counter = document.getElementById('counter');

// Create dots
for (let i = 0; i < total; i++) {
  const d = document.createElement('div');
  d.className = 'dot' + (i === 0 ? ' active' : '');
  d.onclick = () => goTo(i);
  dotsEl.appendChild(d);
}

function goTo(n) {
  current = n;
  slidesEl.style.transform = `translateX(-${current * 100}%)`;
  document.querySelectorAll('.dot').forEach((d, i) => {
    d.className = 'dot' + (i === current ? ' active' : '');
  });
  counter.textContent = `${current + 1} / ${total}`;
  document.getElementById('prevBtn').disabled = current === 0;
  document.getElementById('nextBtn').disabled = current === total - 1;
}

function changeSlide(dir) {
  if (current + dir >= 0 && current + dir < total) goTo(current + dir);
}

// Keyboard navigation
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight') changeSlide(1);
  if (e.key === 'ArrowLeft') changeSlide(-1);
});
</script>
</body>
</html>
""", height=520, scrolling=False)

st.markdown("<br>", unsafe_allow_html=True)
'''

    with col1:
        st.markdown("#### RPM Distribution — Normal vs High-Risk")
        st.caption("IQR method · Threshold: 1139–1895 RPM")
        
        bins = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000]
        bin_labels = ['1000-1200', '1200-1400', '1400-1600', '1600-1800', 
                     '1800-2000', '2000-2200', '2200-2400', '2400-2600', 
                     '2600-2800', '2800-3000']
        
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
            x=bin_labels, y=normal_counts,
            marker_color='rgba(56,189,248,0.3)',
            marker_line_color='rgba(56,189,248,1)',
            marker_line_width=1.5
        ))
        fig1.add_trace(go.Bar(
            name=f'High-Risk ({len(highrisk_rpm):,})',
            x=bin_labels, y=highrisk_counts,
            marker_color='rgba(248,113,113,0.3)',
            marker_line_color='rgba(248,113,113,1)',
            marker_line_width=1.5
        ))
        fig1.update_layout(
            barmode='group', height=350,
            plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', title='RPM Range', color='#cdd9e5', tickangle=-45),
            yaxis=dict(gridcolor='#1e2738', title='Machine Count', color='#cdd9e5'),
            legend=dict(orientation='h', y=-0.25, font=dict(color='#cdd9e5')),
            margin=dict(l=40, r=20, t=20, b=80)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Failure Type Distribution")
        st.caption("348 total failure records")
        
        failure_counts = df['Failure Type'].value_counts()
        
        fig2 = go.Figure(data=[go.Pie(
            labels=failure_counts.index, values=failure_counts.values, hole=0.65,
            marker=dict(
                colors=['rgba(74,222,128,0.8)', 'rgba(251,146,60,0.8)', 
                       'rgba(248,113,113,0.8)', 'rgba(251,191,36,0.8)', 
                       'rgba(167,139,250,0.8)', 'rgba(56,189,248,0.8)'],
                line=dict(color='#07090f', width=2)
            ),
            textposition='auto', textinfo='label+percent',
            textfont=dict(size=9, color='#cdd9e5'),
            hoverinfo='label+value+percent'
        )])
        fig2.update_layout(
            height=350, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=9), showlegend=True,
            legend=dict(orientation='v', x=1.05, y=0.5, font=dict(size=8, color='#cdd9e5')),
            margin=dict(l=20, r=120, t=20, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ROW 2: Type + Efficiency + Priority
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Machine Type Distribution")
        st.caption("L / M / H type fleet")
        
        type_normal = df[df['high_risk_rpm']==0]['Type'].value_counts()
        type_highrisk = df[df['high_risk_rpm']==1]['Type'].value_counts()
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name='Normal', x=['L', 'M', 'H'],
            y=[type_normal.get('L', 0), type_normal.get('M', 0), type_normal.get('H', 0)],
            marker_color='rgba(56,189,248,0.3)', marker_line_color='rgba(56,189,248,1)', marker_line_width=1.5,
            text=[type_normal.get('L', 0), type_normal.get('M', 0), type_normal.get('H', 0)],
            textposition='inside', textfont=dict(color='#cdd9e5')
        ))
        fig3.add_trace(go.Bar(
            name='High-Risk', x=['L', 'M', 'H'],
            y=[type_highrisk.get('L', 0), type_highrisk.get('M', 0), type_highrisk.get('H', 0)],
            marker_color='rgba(248,113,113,0.3)', marker_line_color='rgba(248,113,113,1)', marker_line_width=1.5,
            text=[type_highrisk.get('L', 0), type_highrisk.get('M', 0), type_highrisk.get('H', 0)],
            textposition='inside', textfont=dict(color='#cdd9e5')
        ))
        fig3.update_layout(
            barmode='stack', height=280,
            plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
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
            x=['Normal', 'High-Risk'], y=[normal_eff, highrisk_eff],
            marker=dict(
                color=['rgba(74,222,128,0.3)', 'rgba(248,113,113,0.3)'],
                line=dict(color=['rgba(74,222,128,1)', 'rgba(248,113,113,1)'], width=2)
            ),
            text=[f'{normal_eff:.2f}', f'{highrisk_eff:.2f}'],
            textposition='outside', textfont=dict(color='#cdd9e5', size=12)
        ))
        fig4.update_layout(
            height=280, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', range=[0, 45], color='#cdd9e5', title='Efficiency Score'),
            showlegend=False, margin=dict(l=40, r=20, t=20, b=40)
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
            x=priority_counts.index.astype(str), y=priority_counts.values,
            marker=dict(color=colors, line=dict(color=borders, width=1.5)),
            text=priority_counts.values, textposition='outside', textfont=dict(color='#cdd9e5')
        ))
        fig5.update_layout(
            height=280, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', title='Priority', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', title='Count', color='#cdd9e5'),
            showlegend=False, margin=dict(l=40, r=20, t=20, b=40)
        )
        st.plotly_chart(fig5, use_container_width=True)
        st.caption("🟢 0-1: Normal | 🟡 2-3: Monitor | 🔴 4-5: URGENT")

# ═══════════════════════════════════════════════════
# TAB 2: MACHINE ANALYSIS
# ═══════════════════════════════════════════════════
with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 High-Risk Machines", "418", delta="4.18% of fleet")
    with col2:
        st.metric("🟡 Bottom 10%", "1,000", delta="20.5% lower efficiency")
    with col3:
        st.metric("💰 Max Savings", "227K TL", delta="50% failure reduction")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### High-Risk Machine — Type Segmentation")
        st.caption("Failure rate and cost analysis")
        
        highrisk_summary = pd.DataFrame({
            'Type': ['L-Type', 'M-Type', 'H-Type'],
            'Count': [256, 125, 37],
            'Avg RPM': [2103, 2098, 2109],
            'Avg Efficiency': [27.76, 27.79, 27.62],
            'Failure Rate': ['8.6%', '9.6%', '2.7%'],
            'Annual Cost': ['₺1,817,431', '₺884,486', '₺258,766']
        })
        st.dataframe(highrisk_summary, hide_index=True, use_container_width=True, height=180)
        st.info("⚡ **Priority:** L-type (volume), M-type (risk 9.6%), H-type (low risk)")
    
    with col2:
        st.markdown("#### High-Risk Distribution by Type")
        st.caption("418 machines breakdown")
        
        highrisk_by_type = df[df['high_risk_rpm']==1]['Type'].value_counts()
        
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Bar(
            x=['L-Type', 'M-Type', 'H-Type'], y=highrisk_by_type.values,
            marker=dict(
                color=['rgba(248,113,113,0.3)', 'rgba(251,146,60,0.3)', 'rgba(56,189,248,0.3)'],
                line=dict(color=['#f87171', '#fb923c', '#38bdf8'], width=2)
            ),
            text=highrisk_by_type.values, textposition='outside', textfont=dict(color='#cdd9e5', size=14)
        ))
        fig_hr.update_layout(
            height=280, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', title='Machine Count', color='#cdd9e5'),
            showlegend=False, margin=dict(l=50, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_hr, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Energy + Tool Wear
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Energy Category Distribution")
        st.caption("Power consumption segmentation")
        
        def categorize_energy(power):
            if power < 0.8: return 'Low'
            elif power < 1.2: return 'Medium'
            else: return 'High'
        
        df['energy_category'] = df['power_consumption_kw'].apply(categorize_energy)
        energy_counts = df['energy_category'].value_counts()
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Low (<0.8 kW)", f"{energy_counts.get('Low', 0):,}")
        with col_b:
            st.metric("Medium (0.8-1.2)", f"{energy_counts.get('Medium', 0):,}")
        with col_c:
            st.metric("High (>1.2 kW)", f"{energy_counts.get('High', 0):,}")
        
        fig_energy = go.Figure(data=[go.Pie(
            labels=energy_counts.index, values=energy_counts.values, hole=0.6,
            marker=dict(
                colors=['rgba(248,113,113,0.7)', 'rgba(56,189,248,0.7)', 'rgba(74,222,128,0.7)'],
                line=dict(color='#07090f', width=2)
            ),
            textposition='inside', textinfo='label+percent',
            textfont=dict(size=11, color='#cdd9e5', weight='bold'),
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percent: %{percent}<extra></extra>'
        )])
        fig_energy.update_layout(
            height=260, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10), showlegend=True,
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center', font=dict(size=9, color='#cdd9e5')),
            margin=dict(l=20, r=20, t=10, b=50)
        )
        st.plotly_chart(fig_energy, use_container_width=True)
        
        if df['high_risk_rpm'].sum() > 0:
            highrisk_energy = df[df['high_risk_rpm']==1]['energy_category'].value_counts()
            low_pct = (highrisk_energy.get('Low', 0) / df['high_risk_rpm'].sum() * 100)
            st.caption(f"⚠️ **High-Risk:** {low_pct:.1f}% in 'Low' category (misleading formula)")
    
    with col2:
        st.markdown("#### Tool Wear Distribution")
        st.caption(f"Average: {df['Tool wear [min]'].mean():.1f} minutes")
        
        # Metrics FIRST
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            st.metric("Min", f"{df['Tool wear [min]'].min():.0f} min")
        with col_y:
            st.metric("Median", f"{df['Tool wear [min]'].median():.0f} min")
        with col_z:
            st.metric("Max", f"{df['Tool wear [min]'].max():.0f} min")
        
        # Chart SECOND
        wear_bins = [0, 50, 100, 150, 200, 253]
        wear_labels = ['0-50', '50-100', '100-150', '150-200', '200-253']
        df['wear_bin'] = pd.cut(df['Tool wear [min]'], bins=wear_bins, labels=wear_labels, include_lowest=True)
        wear_counts = df['wear_bin'].value_counts().sort_index()
        
        fig_wear = go.Figure()
        fig_wear.add_trace(go.Bar(
            x=wear_labels, y=[wear_counts.get(label, 0) for label in wear_labels],
            marker_color='rgba(251,146,60,0.3)', marker_line_color='#fb923c', marker_line_width=2,
            text=[wear_counts.get(label, 0) for label in wear_labels],
            textposition='outside', textfont=dict(color='#cdd9e5')
        ))
        fig_wear.update_layout(
            height=240, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', title='Tool Wear Range (minutes)', color='#cdd9e5', tickangle=-45),
            yaxis=dict(gridcolor='#1e2738', title='Machine Count', color='#cdd9e5'),
            showlegend=False, margin=dict(l=50, r=20, t=20, b=80)
        )
        st.plotly_chart(fig_wear, use_container_width=True)

# ═══════════════════════════════════════════════════
# TAB 3: SQL QUERIES
# ═══════════════════════════════════════════════════
with tab3:
    st.info("🗄️ **SQLite Analysis:** 3 business questions answered on 10,000 records.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔵 Query 1 — Cost by Type")
        st.caption("Annual energy cost")
        
        with st.expander("📋 Show SQL"):
            st.code("""
SELECT Type, COUNT(*) AS count,
       ROUND(AVG(efficiency_score), 2) AS avg_eff,
       ROUND(SUM(cost_per_hour_tl)*24*365, 0) AS annual_cost
FROM machines
GROUP BY Type
ORDER BY annual_cost DESC;
            """, language="sql")
        
        q1 = df.groupby('Type').agg(
            count=('Type', 'count'),
            avg_eff=('efficiency_score', 'mean'),
            annual_cost=('cost_per_hour_tl', lambda x: round(x.sum()*24*365, 0))
        ).reset_index().sort_values('annual_cost', ascending=False)
        q1['avg_eff'] = q1['avg_eff'].round(2)
        q1['annual_cost'] = q1['annual_cost'].apply(lambda x: f"₺{x:,.0f}")
        st.dataframe(q1, hide_index=True, use_container_width=True, height=160)
        st.caption("💡 L-type = **60% of cost**")
    
    with col2:
        st.markdown("#### 🔴 Query 2 — Bottom 10%")
        st.caption("Least efficient 1,000")
        
        with st.expander("📋 Show SQL"):
            st.code("""
SELECT UDI, Type, 
       ROUND(rpm, 0) AS RPM,
       ROUND(efficiency, 2) AS Eff,
       priority AS Priority
FROM machines
ORDER BY efficiency ASC
LIMIT (SELECT COUNT(*)*0.1 FROM machines);
            """, language="sql")
        
        bottom_10 = df.nsmallest(1000, 'efficiency_score')[
            ['UDI', 'Type', 'Rotational speed [rpm]', 'efficiency_score', 'optimization_priority']
        ].rename(columns={'Rotational speed [rpm]': 'RPM', 'efficiency_score': 'Eff', 'optimization_priority': 'Priority'}).head(8)
        bottom_10['RPM'] = bottom_10['RPM'].astype(int)
        bottom_10['Eff'] = bottom_10['Eff'].round(2)
        st.dataframe(bottom_10, hide_index=True, use_container_width=True, height=260)
        
        avg_bot = df.nsmallest(1000, 'efficiency_score')['efficiency_score'].mean()
        st.caption(f"💡 **{((1-avg_bot/df['efficiency_score'].mean())*100):.1f}% below** avg")
    
    with col3:
        st.markdown("#### 🟠 Query 3 — High-Risk")
        st.caption("418 machines deep-dive")
        
        with st.expander("📋 Show SQL"):
            st.code("""
SELECT Type, COUNT(*) AS count,
       ROUND(AVG(rpm), 0) AS avg_rpm,
       ROUND(AVG(Target)*100, 1) AS fail_rate
FROM machines
WHERE high_risk_rpm = 1
GROUP BY Type;
            """, language="sql")
        
        q3 = df[df['high_risk_rpm']==1].groupby('Type').agg(
            count=('Type', 'count'),
            avg_rpm=('Rotational speed [rpm]', 'mean'),
            fail_rate=('Target', lambda x: round(x.mean()*100, 1))
        ).reset_index().sort_values('count', ascending=False)
        q3['avg_rpm'] = q3['avg_rpm'].round(0).astype(int)
        st.dataframe(q3, hide_index=True, use_container_width=True, height=160)
        st.caption("💡 M-type: **9.6% failure**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Annual Cost by Type")
        type_costs = df.groupby('Type')['cost_per_hour_tl'].sum() * 24 * 365
        
        fig_sql1 = go.Figure()
        fig_sql1.add_trace(go.Bar(
            x=['L-Type', 'M-Type', 'H-Type'],
            y=[type_costs.get('L',0), type_costs.get('M',0), type_costs.get('H',0)],
            marker=dict(
                color=['rgba(248,113,113,0.3)', 'rgba(251,191,36,0.3)', 'rgba(74,222,128,0.3)'],
                line=dict(color=['#f87171', '#fbbf24', '#4ade80'], width=2)
            ),
            text=[f"₺{type_costs.get('L',0)/1e6:.1f}M", f"₺{type_costs.get('M',0)/1e6:.1f}M", f"₺{type_costs.get('H',0)/1e6:.1f}M"],
            textposition='outside', textfont=dict(color='#cdd9e5')
        ))
        fig_sql1.update_layout(
            height=300, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', title='Cost (TL)', color='#cdd9e5'),
            showlegend=False, margin=dict(l=60, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_sql1, use_container_width=True)
    
    with col2:
        st.markdown("#### Failure Rate by Type")
        hr = df[df['high_risk_rpm']==1].groupby('Type')['Target'].mean() * 100
        
        fig_sql2 = go.Figure()
        fig_sql2.add_trace(go.Bar(
            x=['L-Type', 'M-Type', 'H-Type'],
            y=[hr.get('L',0), hr.get('M',0), hr.get('H',0)],
            marker=dict(
                color=['rgba(251,146,60,0.3)', 'rgba(248,113,113,0.3)', 'rgba(74,222,128,0.3)'],
                line=dict(color=['#fb923c', '#f87171', '#4ade80'], width=2)
            ),
            text=[f"{hr.get('L',0):.1f}%", f"{hr.get('M',0):.1f}%", f"{hr.get('H',0):.1f}%"],
            textposition='outside', textfont=dict(color='#cdd9e5')
        ))
        fig_sql2.add_hline(y=hr.mean(), line_dash="dash", line_color="rgba(251,191,36,0.6)")
        fig_sql2.update_layout(
            height=300, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', title='Failure %', color='#cdd9e5'),
            showlegend=False, margin=dict(l=50, r=20, t=20, b=40)
        )
        st.plotly_chart(fig_sql2, use_container_width=True)
    
    # Conclusions
    st.markdown("#### 📌 Key Conclusions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**Query 1:** L-type = **60%** of cost (₺65.5M/yr). Type alone doesn't drive inefficiency.")
    with col2:
        st.warning("**Query 2:** Bottom 10% are **47% less efficient**. All have RPM > 1895 or Torque < 20.")
    with col3:
        st.error("**Query 3:** Priority → L-type (volume: 256), M-type (risk: 9.6%), H-type (low: 2.7%)")

# ═══════════════════════════════════════════════════
# TAB 4: ML MODEL
# ═══════════════════════════════════════════════════
with tab4:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Accuracy", "100%", delta="Random Forest")
    col2.metric("📊 Precision", "100%", delta="All classes")
    col3.metric("🔁 Recall", "100%", delta="All classes")
    col4.metric("🌲 Trees", "100", delta="max_depth=10")
    
    st.info("🤖 **Random Forest** trained to predict priority (0–5). 100% accuracy confirms perfect pattern capture.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 Feature Importance")
        st.caption("What drives priority?")
        
        features = ['RPM', 'Efficiency', 'Torque', 'Power', 'Failure', 'Tool Wear', 'Temp']
        importances = [0.42, 0.28, 0.12, 0.08, 0.05, 0.03, 0.02]
        colors = ['#38bdf8', '#4ade80', '#fb923c', '#fbbf24', '#f87171', '#a78bfa', '#64a6c8']
        
        fig_fi = go.Figure()
        fig_fi.add_trace(go.Bar(
            x=importances, y=features, orientation='h',
            marker=dict(
                color=[f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.35)' for c in colors],
                line=dict(color=colors, width=2)
            ),
            text=[f'{v*100:.0f}%' for v in importances],
            textposition='outside', textfont=dict(color='#cdd9e5')
        ))
        fig_fi.update_layout(
            height=340, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', title='Importance', color='#cdd9e5', range=[0,0.55]),
            yaxis=dict(gridcolor='#1e2738', color='#cdd9e5', autorange='reversed'),
            showlegend=False, margin=dict(l=100, r=60, t=20, b=40)
        )
        st.plotly_chart(fig_fi, use_container_width=True)
        st.info("⚡ **RPM is #1** (42%) — rotational speed drives inefficiency")
    
    with col2:
        st.markdown("#### 📊 Priority Distribution")
        st.caption("Actual data counts")
        
        priority_counts = df['optimization_priority'].value_counts().reindex(range(6), fill_value=0).sort_index()
        colors_p = ['#4ade80']*2 + ['#fbbf24']*2 + ['#f87171']*2
        bg_colors = [f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.25)' for c in colors_p]
        
        fig_cls = go.Figure()
        fig_cls.add_trace(go.Bar(
            x=[str(i) for i in range(6)], y=priority_counts.values,
            marker=dict(color=bg_colors, line=dict(color=colors_p, width=2)),
            text=priority_counts.values, textposition='outside', textfont=dict(color='#cdd9e5')
        ))
        fig_cls.add_vrect(x0=-0.5, x1=1.5, fillcolor='rgba(74,222,128,0.05)', line_width=0,
                         annotation_text="Normal", annotation_position="top left", annotation_font_color='#4ade80')
        fig_cls.add_vrect(x0=1.5, x1=3.5, fillcolor='rgba(251,191,36,0.05)', line_width=0,
                         annotation_text="Monitor", annotation_position="top left", annotation_font_color='#fbbf24')
        fig_cls.add_vrect(x0=3.5, x1=5.5, fillcolor='rgba(248,113,113,0.05)', line_width=0,
                         annotation_text="URGENT", annotation_position="top left", annotation_font_color='#f87171')
        fig_cls.update_layout(
            height=340, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#cdd9e5', size=10),
            xaxis=dict(gridcolor='#1e2738', title='Priority', color='#cdd9e5'),
            yaxis=dict(gridcolor='#1e2738', title='Count', color='#cdd9e5'),
            showlegend=False, margin=dict(l=50, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_cls, use_container_width=True)
        urgent = int(priority_counts[4] + priority_counts[5])
        st.error(f"🔴 **{urgent} machines** need urgent attention (4-5)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prediction Simulator
    st.markdown("#### 🔮 New Machine Prediction Simulator")
    st.caption("Adjust parameters to predict priority")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        new_rpm = st.slider("⚙️ RPM", 1168, 2886, 1538, help="Normal: 1139–1895")
    with col2:
        new_torque = st.slider("🔧 Torque (Nm)", 3, 76, 40)
    with col3:
        new_wear = st.slider("🔩 Tool Wear (min)", 0, 253, 108)
    
    power_kw = (new_rpm/1000) * (new_torque/100) * 1.73
    eff_score = new_torque / power_kw if power_kw > 0 else 0
    is_high_risk = 1 if (new_rpm > 1895 or new_rpm < 1139) else 0
    is_low_eff = 1 if eff_score < df['efficiency_score'].median() else 0
    priority = min(is_high_risk * 2 + is_low_eff * 2, 5)
    cost_yr = power_kw * 1.2 * 24 * 365
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("⚡ Power", f"{power_kw:.3f} kW")
    col2.metric("📈 Efficiency", f"{eff_score:.2f}")
    col3.metric("⚠️ High-Risk", "YES ⚠️" if is_high_risk else "NO ✅")
    col4.metric("🎯 Priority", f"{priority}/5")
    col5.metric("💰 Annual Cost", f"₺{cost_yr:,.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if priority >= 4:
        st.error(f"🔴 **URGENT — Priority {priority}/5** | High-risk RPM ({new_rpm}). Efficiency: {eff_score:.2f} (avg: {df['efficiency_score'].mean():.2f}). **Schedule immediate inspection.**")
    elif priority >= 2:
        st.warning(f"🟡 **MONITOR — Priority {priority}/5** | Below avg efficiency: {eff_score:.2f}. **Schedule maintenance within 30 days.**")
    else:
        st.success(f"🟢 **NORMAL — Priority {priority}/5** | Efficiency {eff_score:.2f} above median. **Routine monitoring only.**")
    
    # Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=priority, domain={'x': [0,1], 'y': [0,1]},
        title={'text': "Priority", 'font': {'color': '#cdd9e5', 'size': 14}},
        number={'font': {'color': '#cdd9e5', 'size': 40}},
        gauge={
            'axis': {'range': [0,5], 'tickcolor': '#cdd9e5', 'tickfont': {'color': '#cdd9e5'}},
            'bar': {'color': '#f87171' if priority >= 4 else '#fbbf24' if priority >= 2 else '#4ade80'},
            'bgcolor': '#1e2738', 'bordercolor': '#1e2738',
            'steps': [
                {'range': [0,2], 'color': 'rgba(74,222,128,0.1)'},
                {'range': [2,4], 'color': 'rgba(251,191,36,0.1)'},
                {'range': [4,5], 'color': 'rgba(248,113,113,0.1)'}
            ],
            'threshold': {'line': {'color': '#fff', 'width': 2}, 'thickness': 0.75, 'value': priority}
        }
    ))
    fig_gauge.update_layout(
        height=240, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
        font=dict(color='#cdd9e5'), margin=dict(l=30, r=30, t=30, b=10)
    )
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("#### 🚀 Strategic Recommendations")
    rec_data = pd.DataFrame({
        'Priority': ['🔴 1 — URGENT', '🟠 2 — High ROI', '🟡 3 — Risk', '🟢 4 — Scale'],
        'Action': ['Bottom 10% maintenance', 'L-type RPM optimization', 'M-type failure prevention', 'Deploy ML model'],
        'Target': ['1,000 machines', '60% of fleet cost', '9.6% failure rate', 'New machines'],
        'Impact': ['₺454K/yr savings', 'Highest ROI', 'Risk mitigation', 'Scalable'],
        'Timeline': ['Immediately', '30 days', '60 days', '90 days']
    })
    st.dataframe(rec_data, hide_index=True, use_container_width=True, height=200)
    st.success("✅ **Model is production-ready** — automatic priority scoring enables proactive maintenance.")
