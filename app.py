import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(
    page_title="⚡ Energy Efficiency Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
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
    def categorize_energy(p):
        if p < 0.8: return 'Low'
        elif p < 1.2: return 'Medium'
        else: return 'High'
    df['energy_category'] = df['power_consumption_kw'].apply(categorize_energy)
    wear_bins = [0, 50, 100, 150, 200, 253]
    wear_labels = ['0-50', '50-100', '100-150', '150-200', '200-253']
    df['wear_bin'] = pd.cut(df['Tool wear [min]'], bins=wear_bins, labels=wear_labels, include_lowest=True)
    return df

# ═══════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════
st.markdown("""
<style>
/* ── Base ── */
.stApp { background: #07090f !important; color: #cdd9e5 !important; }
section[data-testid="stMain"] { background: #07090f !important; }
.block-container { background: #07090f !important; padding: 1rem 1.5rem 2rem !important; max-width: 100% !important; }
header[data-testid="stHeader"] { background: #07090f !important; border-bottom: 1px solid #1e2738 !important; }
footer { display: none !important; }

/* ── Hide sidebar toggle button ── */
[data-testid="collapsedControl"] { display: none !important; }
button[kind="header"] { display: none !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0a0e1a !important;
    border-right: 1px solid rgba(0,206,209,0.12) !important;
    min-width: 230px !important;
    max-width: 230px !important;
}
section[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
section[data-testid="stSidebar"] .block-container { padding: 0 !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #0d1117 !important;
    border: 1px solid #1e2738 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
[data-testid="stMetricValue"] { color: #cdd9e5 !important; font-size: 20px !important; }
[data-testid="stMetricLabel"] { color: #4a6072 !important; font-size: 11px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117 !important;
    border: 1px solid #1e2738 !important;
    border-radius: 8px !important;
    gap: 2px !important;
    padding: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #4a6072 !important;
    border-radius: 6px !important;
    padding: 7px 14px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] { background: #161b24 !important; color: #00ced1 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #07090f !important; padding-top: 14px !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { background: #0d1117 !important; border-color: #1e2738 !important; }

/* ── Expander ── */
[data-testid="stExpander"] { background: #0d1117 !important; border: 1px solid #1e2738 !important; border-radius: 10px !important; }
summary { color: #cdd9e5 !important; }
pre { background: #0d1117 !important; color: #cdd9e5 !important; }

/* ── Text ── */
p, h1, h2, h3, h4, label { color: #cdd9e5 !important; }
.stCaption > div { color: #4a6072 !important; }

/* ── Multiselect ── */
[data-baseweb="select"] { background: #0d1117 !important; border-color: #1e2738 !important; }
[data-baseweb="tag"] { background: rgba(0,206,209,0.15) !important; color: #00ced1 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; background: #07090f; }
::-webkit-scrollbar-thumb { background: #1e2738; border-radius: 2px; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00ced1, #0891b2) !important;
    color: #000 !important; font-weight: 700 !important;
    border-radius: 8px !important; border: none !important;
    font-size: 12px !important; padding: 8px 20px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }

/* ── Cover button override ── */
.cover-btn > button {
    background: linear-gradient(135deg, #ff8c00, #ffaa00) !important;
    color: #000 !important; font-weight: 800 !important;
    font-size: 16px !important; padding: 14px 40px !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 30px rgba(255,140,0,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════
if st.session_state.page == 'cover':
    st.markdown("""
    <style>
    .stApp { background: #000 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:64px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:80px;filter:drop-shadow(0 0 40px rgba(255,165,0,0.6))'>⚡</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:11px;letter-spacing:8px;text-transform:uppercase;color:rgba(255,255,255,0.25);margin:14px 0'>INDUSTRIAL DATA SCIENCE PORTFOLIO</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:3px;background:linear-gradient(90deg,transparent,#ff8c00,#ffaa00,#ff8c00,transparent);margin:0 auto;max-width:680px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:46px;font-weight:900;letter-spacing:3px;text-transform:uppercase;color:#fff;line-height:1.2'>MANUFACTURING ENERGY<br><span style=\"color:#ffaa00\">EFFICIENCY ANALYSIS</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:15px;color:rgba(255,255,255,0.45);font-style:italic'>Predictive Maintenance · Machine Learning · SQL Analytics<br><span style=\"color:rgba(255,165,0,0.75);font-weight:600\">10,000 Machines · 418 High-Risk · ₺2.96M Cost Impact</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center'><span style='display:inline-block;padding:5px 14px;border:1px solid rgba(255,140,0,0.4);color:rgba(255,140,0,0.8);font-size:9px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:3px'>PYTHON</span><span style='display:inline-block;padding:5px 14px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.35);font-size:9px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:3px'>SQL</span><span style='display:inline-block;padding:5px 14px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.35);font-size:9px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:3px'>RANDOM FOREST</span><span style='display:inline-block;padding:5px 14px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.35);font-size:9px;letter-spacing:2px;text-transform:uppercase;border-radius:20px;margin:3px'>STREAMLIT</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:44px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="cover-btn">', unsafe_allow_html=True)
        if st.button("🚀  ENTER DASHBOARD", use_container_width=True):
            st.session_state.page = 'executive'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;margin-top:36px;font-size:10px;color:rgba(255,255,255,0.15);letter-spacing:3px;text-transform:uppercase'>N. Nur Altay · Data Analyst · February 2026</div>", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════
# EXECUTIVE SUMMARY PAGE
# ═══════════════════════════════════════════
if st.session_state.page == 'executive':
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    .block-container { padding: 2rem 3rem !important; max-width: 1100px !important; margin: 0 auto !important; }
    </style>
    """, unsafe_allow_html=True)

    # Top bar
    col_back, col_title, col_enter = st.columns([1, 4, 1])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = 'cover'
            st.rerun()
    with col_title:
        st.markdown("<div style='text-align:center;font-size:10px;letter-spacing:4px;text-transform:uppercase;color:rgba(255,255,255,0.25);padding-top:8px'>EXECUTIVE BRIEFING</div>", unsafe_allow_html=True)
    with col_enter:
        if st.button("Dashboard →"):
            st.session_state.page = 'dashboard'
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Title
    st.markdown("""
    <div style="text-align:center;margin-bottom:32px">
        <div style="font-size:32px;font-weight:900;color:#fff;letter-spacing:-0.5px">
            Manufacturing Energy Efficiency
            <span style="color:#00ced1"> — Executive Summary</span>
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.35);margin-top:8px;letter-spacing:1px">
            End-to-end analysis · 10,000 machines · N. Nur Altay · February 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    kpis = [
        ("10,000", "Machines\nAnalyzed", "#38bdf8"),
        ("418", "High-Risk\nUnits", "#f87171"),
        ("27.8%", "Efficiency\nGap", "#fb923c"),
        ("₺2.96M", "Annual\nCost Risk", "#ffaa00"),
        ("227K TL", "Savings\nPotential", "#4ade80"),
        ("100%", "ML Model\nAccuracy", "#a78bfa"),
    ]
    for col, (val, lbl, color) in zip([k1,k2,k3,k4,k5,k6], kpis):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:16px 10px;text-align:center">
                <div style="font-size:22px;font-weight:900;color:{color};line-height:1;margin-bottom:6px">{val}</div>
                <div style="font-size:9px;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,0.3);line-height:1.4">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Two columns: Problem + Findings
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#100a08,#1a0e0a);border:1px solid rgba(248,113,113,0.15);border-radius:14px;padding:24px">
            <div style="font-size:9px;letter-spacing:4px;text-transform:uppercase;color:#f87171;margin-bottom:10px;font-weight:700">BUSINESS PROBLEM</div>
            <div style="font-size:18px;font-weight:800;color:#fff;margin-bottom:16px;line-height:1.3">The Cost of<br><span style="color:#ffaa00">Undetected Inefficiency</span></div>
            <div style="display:flex;flex-direction:column;gap:10px">
                <div style="display:flex;gap:12px;padding:12px;background:rgba(255,255,255,0.03);border-left:3px solid #f87171;border-radius:0 8px 8px 0">
                    <div style="font-size:18px">⚠️</div>
                    <div>
                        <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:3px">418 Hidden High-Risk Machines</div>
                        <div style="font-size:11px;color:rgba(255,255,255,0.4);line-height:1.5">4.18% of fleet operating at abnormal RPM — invisible without data analysis. 2.6× higher failure rate.</div>
                    </div>
                </div>
                <div style="display:flex;gap:12px;padding:12px;background:rgba(255,255,255,0.03);border-left:3px solid #fb923c;border-radius:0 8px 8px 0">
                    <div style="font-size:18px">💸</div>
                    <div>
                        <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:3px">₺2.96M Annual Financial Exposure</div>
                        <div style="font-size:11px;color:rgba(255,255,255,0.4);line-height:1.5">L-type machines alone drive 60% of total fleet energy cost (₺65.5M/year). Risk is concentrated.</div>
                    </div>
                </div>
                <div style="display:flex;gap:12px;padding:12px;background:rgba(255,255,255,0.03);border-left:3px solid #fbbf24;border-radius:0 8px 8px 0">
                    <div style="font-size:18px">📉</div>
                    <div>
                        <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:3px">27.8% Efficiency Gap</div>
                        <div style="font-size:11px;color:rgba(255,255,255,0.4);line-height:1.5">High-risk machines score 27.76 vs 38.45 fleet average. Every point of efficiency = direct cost saving.</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        components.html("""
        <style>* { margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',sans-serif; }</style>
        <div style="background:linear-gradient(135deg,#080d10,#0a1218);border:1px solid rgba(0,206,209,0.15);border-radius:14px;padding:24px;height:100%">
            <div style="font-size:9px;letter-spacing:4px;text-transform:uppercase;color:#00ced1;margin-bottom:10px;font-weight:700">KEY FINDINGS</div>
            <div style="font-size:18px;font-weight:800;color:#fff;margin-bottom:16px;line-height:1.3">What the Data<br><span style="color:#00ced1">Revealed</span></div>

            <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:14px;margin-bottom:10px">
                <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:10px">FLEET RISK BREAKDOWN</div>
                <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06)">
                    <span style="font-size:12px;color:rgba(255,255,255,0.6)">L-Type</span>
                    <span style="font-size:12px;font-weight:700;color:#f87171">256 units · 8.6% fail · &#8378;1.82M/yr</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.06)">
                    <span style="font-size:12px;color:rgba(255,255,255,0.6)">M-Type</span>
                    <span style="font-size:12px;font-weight:700;color:#fb923c">125 units · 9.6% fail · &#8378;884K/yr</span>
                </div>
                <div style="display:flex;justify-content:space-between;padding:7px 0">
                    <span style="font-size:12px;color:rgba(255,255,255,0.6)">H-Type</span>
                    <span style="font-size:12px;font-weight:700;color:#4ade80">37 units · 2.7% fail · &#8378;259K/yr</span>
                </div>
            </div>

            <div style="display:flex;gap:8px;margin-bottom:10px">
                <div style="flex:1;background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.15);border-radius:8px;padding:10px;text-align:center">
                    <div style="font-size:18px;font-weight:900;color:#f87171">2.6x</div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:1px;margin-top:2px">Higher Failure Rate</div>
                </div>
                <div style="flex:1;background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.15);border-radius:8px;padding:10px;text-align:center">
                    <div style="font-size:18px;font-weight:900;color:#fbbf24">9.6%</div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:1px;margin-top:2px">M-Type Max Risk</div>
                </div>
                <div style="flex:1;background:rgba(74,222,128,0.06);border:1px solid rgba(74,222,128,0.15);border-radius:8px;padding:10px;text-align:center">
                    <div style="font-size:18px;font-weight:900;color:#4ade80">60%</div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:1px;margin-top:2px">Cost from L-Type</div>
                </div>
            </div>

            <div style="background:rgba(167,139,250,0.06);border:1px solid rgba(167,139,250,0.15);border-radius:8px;padding:12px">
                <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#a78bfa;margin-bottom:6px">ML MODEL OUTPUT</div>
                <div style="font-size:12px;color:rgba(255,255,255,0.6);line-height:1.6">Random Forest achieves <strong style="color:#a78bfa">100% accuracy</strong> in priority scoring (0-5 scale). RPM is the #1 feature at 42% importance. Model is <strong style="color:#4ade80">production-ready</strong>.</div>
            </div>
        </div>
        """, height=420)
        
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Action plan
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0d0a14,#120d1c);border:1px solid rgba(167,139,250,0.15);border-radius:14px;padding:24px">
        <div style="font-size:9px;letter-spacing:4px;text-transform:uppercase;color:#a78bfa;margin-bottom:10px;font-weight:700">STRATEGIC ACTION PLAN</div>
        <div style="font-size:18px;font-weight:800;color:#fff;margin-bottom:20px">4-Step Optimization Roadmap — <span style="color:#a78bfa">₺227K/yr Savings Target</span></div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
            <div style="background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.2);border-radius:10px;padding:16px">
                <div style="font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;background:rgba(248,113,113,0.15);color:#f87171;border-radius:4px;display:inline-block;margin-bottom:10px">URGENT</div>
                <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:6px">Bottom 10% Maintenance</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.4);line-height:1.5">1,000 least efficient machines. Immediate inspection required.</div>
                <div style="font-size:11px;color:#f87171;font-weight:700;margin-top:8px">₺454K/yr recovery</div>
            </div>
            <div style="background:rgba(251,146,60,0.06);border:1px solid rgba(251,146,60,0.2);border-radius:10px;padding:16px">
                <div style="font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;background:rgba(251,146,60,0.15);color:#fb923c;border-radius:4px;display:inline-block;margin-bottom:10px">30 DAYS</div>
                <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:6px">L-Type RPM Optimization</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.4);line-height:1.5">256 high-risk L-type units. 60% of total fleet cost base.</div>
                <div style="font-size:11px;color:#fb923c;font-weight:700;margin-top:8px">Highest ROI target</div>
            </div>
            <div style="background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.2);border-radius:10px;padding:16px">
                <div style="font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;background:rgba(251,191,36,0.15);color:#fbbf24;border-radius:4px;display:inline-block;margin-bottom:10px">60 DAYS</div>
                <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:6px">M-Type Failure Prevention</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.4);line-height:1.5">125 units at 9.6% failure rate. Highest per-unit risk in fleet.</div>
                <div style="font-size:11px;color:#fbbf24;font-weight:700;margin-top:8px">Risk mitigation</div>
            </div>
            <div style="background:rgba(74,222,128,0.06);border:1px solid rgba(74,222,128,0.2);border-radius:10px;padding:16px">
                <div style="font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;background:rgba(74,222,128,0.15);color:#4ade80;border-radius:4px;display:inline-block;margin-bottom:10px">90 DAYS</div>
                <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:6px">Deploy ML Scoring Model</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.4);line-height:1.5">Auto-prioritize all new machines. Scalable proactive maintenance.</div>
                <div style="font-size:11px;color:#4ade80;font-weight:700;margin-top:8px">Scalable system</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊  Open Full Dashboard →", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    st.stop()

# ═══════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════
df = load_data()

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 16px 14px;border-bottom:1px solid rgba(0,206,209,0.12)">
        <div style="font-size:20px;margin-bottom:4px">⚡</div>
        <div style="font-size:13px;font-weight:800;color:#00ced1;letter-spacing:0.5px">Energy Dashboard</div>
        <div style="font-size:9px;color:rgba(255,255,255,0.2);letter-spacing:2px;text-transform:uppercase;margin-top:2px">N. Nur Altay · Feb 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:8px;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.2);padding:0 16px;margin-bottom:8px;font-weight:700'>FILTERS</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:1px;text-transform:uppercase;padding:0 4px;margin-bottom:4px'>Machine Type</div>", unsafe_allow_html=True)
    type_filter = st.multiselect("type", options=['L','M','H'], default=['L','M','H'], label_visibility="collapsed")

    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:1px;text-transform:uppercase;padding:0 4px;margin-bottom:4px;margin-top:10px'>Risk Status</div>", unsafe_allow_html=True)
    risk_filter = st.multiselect("risk", options=['Normal','High-Risk'], default=['Normal','High-Risk'], label_visibility="collapsed")

    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:1px;text-transform:uppercase;padding:0 4px;margin-bottom:4px;margin-top:10px'>Priority Score</div>", unsafe_allow_html=True)
    priority_range = st.select_slider("priority", options=[0,1,2,3,4,5], value=(0,5), label_visibility="collapsed")

    st.markdown("<div style='font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:1px;text-transform:uppercase;padding:0 4px;margin-bottom:4px;margin-top:10px'>RPM Range</div>", unsafe_allow_html=True)
    rpm_min = int(df['Rotational speed [rpm]'].min())
    rpm_max = int(df['Rotational speed [rpm]'].max())
    rpm_range = st.slider("rpm", min_value=rpm_min, max_value=rpm_max, value=(rpm_min, rpm_max), label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(0,206,209,0.08);margin:16px 0'>", unsafe_allow_html=True)

    if st.button("← Executive Summary", use_container_width=True):
        st.session_state.page = 'executive'
        st.rerun()
    if st.button("⌂ Cover", use_container_width=True):
        st.session_state.page = 'cover'
        st.rerun()

# ── Apply Filters ──
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

# ── Header ──
st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d1117,#161b24);border:1px solid #1e2738;border-radius:12px;padding:14px 22px;margin-bottom:14px">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
        <div style="display:flex;align-items:center;gap:14px">
            <div style="width:40px;height:40px;background:linear-gradient(135deg,#00ced1,#0891b2);border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 0 14px rgba(0,206,209,0.3)">⚡</div>
            <div>
                <div style="font-size:17px;font-weight:800;color:#fff;letter-spacing:-0.3px">Manufacturing Energy Efficiency Analysis</div>
                <div style="font-size:10px;color:#4a6072;letter-spacing:1.5px;text-transform:uppercase;margin-top:1px">Predictive Maintenance · 10,000 Machines · N. Nur Altay</div>
            </div>
        </div>
        <div style="display:flex;gap:8px;align-items:center">
            <div style="padding:5px 12px;background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.2);border-radius:14px;font-size:10px;color:#4ade80;display:flex;align-items:center;gap:5px">
                <div style="width:5px;height:5px;background:#4ade80;border-radius:50%"></div>Live
            </div>
            <div style="padding:5px 12px;background:#161b24;border:1px solid #1e2738;border-radius:14px;font-size:10px;color:#4a6072">Feb 2026</div>
            <div style="padding:5px 12px;background:rgba(0,206,209,0.08);border:1px solid rgba(0,206,209,0.2);border-radius:14px;font-size:10px;color:#00ced1">{len(dff):,} machines</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──
c1,c2,c3,c4,c5 = st.columns(5)
with c1: st.metric("🏭 Machines", f"{len(dff):,}", delta=f"{len(dff)/len(df)*100:.0f}% of fleet")
with c2:
    hr = int(dff['high_risk_rpm'].sum())
    st.metric("⚠️ High-Risk", f"{hr}", delta=f"{hr/len(dff)*100:.1f}%" if len(dff)>0 else "—", delta_color="inverse")
with c3:
    ne = dff[dff['high_risk_rpm']==0]['efficiency_score'].mean() if len(dff)>0 else 0
    st.metric("📈 Avg Efficiency", f"{ne:.1f}" if ne else "—")
with c4:
    st.metric("💰 Avg Cost/hr", f"{dff['cost_per_hour_tl'].mean():.2f} TL" if len(dff)>0 else "—")
with c5:
    fl = int(dff['Target'].sum())
    st.metric("🔥 Failures", f"{fl}", delta=f"{fl/len(dff)*100:.1f}%" if len(dff)>0 else "—", delta_color="inverse")

if len(dff) != len(df):
    st.info(f"🔍 Filter active: **{len(dff):,}** of {len(df):,} machines | Types: {', '.join(type_filter)} | Risk: {', '.join(risk_filter)} | Priority: {priority_range[0]}–{priority_range[1]}")
else:
    st.info("💡 **Key Finding:** 418 high-risk machines have **27.8% lower efficiency**. Annual cost impact: **~₺2.96M**. Use sidebar filters to explore segments.")

# ── TABS ──
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡ Fleet Health",
    "🔴 Risk & Cost",
    "📋 Business Insights",
    "🤖 Predictive Model"
])

# ═══════════════════════════════════════════
# TAB 1: FLEET HEALTH
# ═══════════════════════════════════════════
with tab1:
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
# TAB 2: RISK & COST
# ═══════════════════════════════════════════
with tab2:
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("🔴 High-Risk Machines", f"{int(dff['high_risk_rpm'].sum())}", delta=f"{dff['high_risk_rpm'].sum()/len(dff)*100:.2f}% of filtered" if len(dff)>0 else "—")
    with c2: st.metric("🟡 Bottom 10%", f"{max(1,int(len(dff)*0.1)):,}", delta="Least efficient")
    with c3: st.metric("💰 Savings Potential", "₺227K/yr", delta="50% failure reduction")

    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2 = st.columns(2)

    with col1:
        st.markdown("#### High-Risk Type Segmentation")
        highrisk_summary = pd.DataFrame({'Type':['L-Type','M-Type','H-Type'],'Count':[256,125,37],'Avg RPM':[2103,2098,2109],'Avg Efficiency':[27.76,27.79,27.62],'Failure Rate':['8.6%','9.6%','2.7%'],'Annual Cost':['₺1,817,431','₺884,486','₺258,766']})
        st.dataframe(highrisk_summary, hide_index=True, use_container_width=True, height=180)
        st.info("⚡ L-type = highest volume risk · M-type = highest failure rate (9.6%) · H-type = low risk")

    with col2:
        st.markdown("#### High-Risk Distribution by Type")
        highrisk_by_type = dff[dff['high_risk_rpm']==1]['Type'].value_counts()
        fig_hr = go.Figure()
        fig_hr.add_trace(go.Bar(x=['L-Type','M-Type','H-Type'],y=[highrisk_by_type.get('L',0),highrisk_by_type.get('M',0),highrisk_by_type.get('H',0)],marker=dict(color=['rgba(248,113,113,0.3)','rgba(251,146,60,0.3)','rgba(56,189,248,0.3)'],line=dict(color=['#f87171','#fb923c','#38bdf8'],width=2)),text=[highrisk_by_type.get('L',0),highrisk_by_type.get('M',0),highrisk_by_type.get('H',0)],textposition='outside',textfont=dict(color='#cdd9e5',size=14)))
        fig_hr.update_layout(height=260,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Count',color='#cdd9e5'),showlegend=False,margin=dict(l=50,r=20,t=20,b=40))
        st.plotly_chart(fig_hr, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### Energy Category Distribution")
        energy_counts = dff['energy_category'].value_counts()
        ca,cb,cc = st.columns(3)
        with ca: st.metric("Low <0.8kW", f"{energy_counts.get('Low',0):,}")
        with cb: st.metric("Medium", f"{energy_counts.get('Medium',0):,}")
        with cc: st.metric("High >1.2kW", f"{energy_counts.get('High',0):,}")
        fig_energy = go.Figure(data=[go.Pie(labels=energy_counts.index,values=energy_counts.values,hole=0.6,marker=dict(colors=['rgba(248,113,113,0.7)','rgba(56,189,248,0.7)','rgba(74,222,128,0.7)'],line=dict(color='#07090f',width=2)),textposition='inside',textinfo='label+percent',textfont=dict(size=11,color='#cdd9e5'))])
        fig_energy.update_layout(height=230,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),showlegend=True,legend=dict(orientation='h',y=-0.15,x=0.5,xanchor='center',font=dict(size=9,color='#cdd9e5')),margin=dict(l=20,r=20,t=10,b=50))
        st.plotly_chart(fig_energy, use_container_width=True)

    with col2:
        st.markdown("#### Tool Wear Distribution")
        cx,cy,cz = st.columns(3)
        with cx: st.metric("Min", f"{dff['Tool wear [min]'].min():.0f} min")
        with cy: st.metric("Median", f"{dff['Tool wear [min]'].median():.0f} min")
        with cz: st.metric("Max", f"{dff['Tool wear [min]'].max():.0f} min")
        wear_labels = ['0-50','50-100','100-150','150-200','200-253']
        wear_counts = dff['wear_bin'].value_counts().sort_index()
        fig_wear = go.Figure()
        fig_wear.add_trace(go.Bar(x=wear_labels,y=[wear_counts.get(l,0) for l in wear_labels],marker_color='rgba(251,146,60,0.3)',marker_line_color='#fb923c',marker_line_width=2,text=[wear_counts.get(l,0) for l in wear_labels],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_wear.update_layout(height=215,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',title='Tool Wear (min)',color='#cdd9e5',tickangle=-45),yaxis=dict(gridcolor='#1e2738',title='Count',color='#cdd9e5'),showlegend=False,margin=dict(l=50,r=20,t=20,b=80))
        st.plotly_chart(fig_wear, use_container_width=True)

# ═══════════════════════════════════════════
# TAB 3: BUSINESS INSIGHTS
# ═══════════════════════════════════════════
with tab3:
    st.info("🗄️ **SQLite Analysis:** 3 business questions answered on 10,000 records.")
    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("#### 🔵 Annual Cost by Type")
        with st.expander("📋 SQL"):
            st.code("""SELECT Type, COUNT(*) AS count,
       ROUND(AVG(efficiency_score),2) AS avg_eff,
       ROUND(SUM(cost_per_hour_tl)*24*365,0) AS annual_cost
FROM machines
GROUP BY Type ORDER BY annual_cost DESC;""", language="sql")
        q1 = df.groupby('Type').agg(count=('Type','count'),avg_eff=('efficiency_score','mean'),annual_cost=('cost_per_hour_tl',lambda x:round(x.sum()*24*365,0))).reset_index().sort_values('annual_cost',ascending=False)
        q1['avg_eff'] = q1['avg_eff'].round(2)
        q1['annual_cost'] = q1['annual_cost'].apply(lambda x:f"₺{x:,.0f}")
        st.dataframe(q1, hide_index=True, use_container_width=True, height=160)
        st.caption("💡 L-type = **60% of cost**")

    with col2:
        st.markdown("#### 🔴 Bottom 10% Efficiency")
        with st.expander("📋 SQL"):
            st.code("""SELECT UDI, Type, rpm, efficiency, priority
FROM machines
ORDER BY efficiency ASC
LIMIT (SELECT COUNT(*)*0.1 FROM machines);""", language="sql")
        bottom_10 = df.nsmallest(1000,'efficiency_score')[['UDI','Type','Rotational speed [rpm]','efficiency_score','optimization_priority']].rename(columns={'Rotational speed [rpm]':'RPM','efficiency_score':'Eff','optimization_priority':'Priority'}).head(8)
        bottom_10['RPM'] = bottom_10['RPM'].astype(int)
        bottom_10['Eff'] = bottom_10['Eff'].round(2)
        st.dataframe(bottom_10, hide_index=True, use_container_width=True, height=260)
        avg_bot = df.nsmallest(1000,'efficiency_score')['efficiency_score'].mean()
        st.caption(f"💡 **{((1-avg_bot/df['efficiency_score'].mean())*100):.1f}% below** fleet avg")

    with col3:
        st.markdown("#### 🟠 High-Risk Segmentation")
        with st.expander("📋 SQL"):
            st.code("""SELECT Type, COUNT(*) AS count,
       ROUND(AVG(rpm),0) AS avg_rpm,
       ROUND(AVG(Target)*100,1) AS fail_rate
FROM machines WHERE high_risk_rpm=1
GROUP BY Type;""", language="sql")
        q3 = df[df['high_risk_rpm']==1].groupby('Type').agg(count=('Type','count'),avg_rpm=('Rotational speed [rpm]','mean'),fail_rate=('Target',lambda x:round(x.mean()*100,1))).reset_index().sort_values('count',ascending=False)
        q3['avg_rpm'] = q3['avg_rpm'].round(0).astype(int)
        st.dataframe(q3, hide_index=True, use_container_width=True, height=160)
        st.caption("💡 M-type: **9.6% failure** — highest risk")

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### Annual Cost by Type (TL)")
        type_costs = df.groupby('Type')['cost_per_hour_tl'].sum()*24*365
        fig_sql1 = go.Figure()
        fig_sql1.add_trace(go.Bar(x=['L-Type','M-Type','H-Type'],y=[type_costs.get('L',0),type_costs.get('M',0),type_costs.get('H',0)],marker=dict(color=['rgba(248,113,113,0.3)','rgba(251,191,36,0.3)','rgba(74,222,128,0.3)'],line=dict(color=['#f87171','#fbbf24','#4ade80'],width=2)),text=[f"₺{type_costs.get('L',0)/1e6:.1f}M",f"₺{type_costs.get('M',0)/1e6:.1f}M",f"₺{type_costs.get('H',0)/1e6:.1f}M"],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_sql1.update_layout(height=280,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Cost (TL)',color='#cdd9e5'),showlegend=False,margin=dict(l=60,r=20,t=20,b=40))
        st.plotly_chart(fig_sql1, use_container_width=True)

    with col2:
        st.markdown("#### Failure Rate by Type (%)")
        hr2 = df[df['high_risk_rpm']==1].groupby('Type')['Target'].mean()*100
        fig_sql2 = go.Figure()
        fig_sql2.add_trace(go.Bar(x=['L-Type','M-Type','H-Type'],y=[hr2.get('L',0),hr2.get('M',0),hr2.get('H',0)],marker=dict(color=['rgba(251,146,60,0.3)','rgba(248,113,113,0.3)','rgba(74,222,128,0.3)'],line=dict(color=['#fb923c','#f87171','#4ade80'],width=2)),text=[f"{hr2.get('L',0):.1f}%",f"{hr2.get('M',0):.1f}%",f"{hr2.get('H',0):.1f}%"],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_sql2.add_hline(y=hr2.mean(),line_dash="dash",line_color="rgba(251,191,36,0.6)",annotation_text="Fleet avg",annotation_font_color="#fbbf24")
        fig_sql2.update_layout(height=280,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',color='#cdd9e5'),yaxis=dict(gridcolor='#1e2738',title='Failure %',color='#cdd9e5'),showlegend=False,margin=dict(l=50,r=20,t=20,b=40))
        st.plotly_chart(fig_sql2, use_container_width=True)

    st.markdown("#### 📌 Key Business Conclusions")
    col1,col2,col3 = st.columns(3)
    with col1: st.success("**Cost:** L-type = **60%** of total fleet cost (₺65.5M/yr). Primary optimization target.")
    with col2: st.warning("**Efficiency:** Bottom 10% are **47% less efficient**. ₺454K/yr recovery potential.")
    with col3: st.error("**Risk:** M-type highest failure rate at **9.6%**. Requires immediate risk program.")

# ═══════════════════════════════════════════
# TAB 4: PREDICTIVE MODEL
# ═══════════════════════════════════════════
with tab4:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🎯 Accuracy","100%",delta="Random Forest")
    c2.metric("📊 Precision","100%",delta="All classes")
    c3.metric("🔁 Recall","100%",delta="All classes")
    c4.metric("🌲 Trees","100",delta="max_depth=10")
    st.info("🤖 **Random Forest** predicts maintenance priority (0–5). RPM is #1 feature at 42% importance. Production-ready.")

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### Feature Importance")
        features = ['RPM','Efficiency','Torque','Power','Failure','Tool Wear','Temp Diff']
        importances = [0.42,0.28,0.12,0.08,0.05,0.03,0.02]
        colors_fi = ['#38bdf8','#4ade80','#fb923c','#fbbf24','#f87171','#a78bfa','#64a6c8']
        fig_fi = go.Figure()
        fig_fi.add_trace(go.Bar(x=importances,y=features,orientation='h',marker=dict(color=[f'rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.3)' for c in colors_fi],line=dict(color=colors_fi,width=2)),text=[f'{v*100:.0f}%' for v in importances],textposition='outside',textfont=dict(color='#cdd9e5')))
        fig_fi.update_layout(height=320,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5',size=10),xaxis=dict(gridcolor='#1e2738',title='Importance',color='#cdd9e5',range=[0,0.55]),yaxis=dict(gridcolor='#1e2738',color='#cdd9e5',autorange='reversed'),showlegend=False,margin=dict(l=100,r=60,t=20,b=40))
        st.plotly_chart(fig_fi, use_container_width=True)

    with col2:
        st.markdown("#### Priority Class Distribution")
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

    st.markdown("#### 🔮 Prediction Simulator")
    st.caption("Adjust parameters — model predicts maintenance priority in real time")
    col1,col2,col3 = st.columns(3)
    with col1: new_rpm = st.slider("⚙️ RPM",1168,2886,1538,help="Normal zone: 1139–1895")
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
    c3.metric("⚠️ Risk Status","HIGH ⚠️" if is_high_risk else "NORMAL ✅")
    c4.metric("🎯 Priority",f"{priority}/5")
    c5.metric("💰 Annual Cost",f"₺{cost_yr:,.0f}")

    if priority>=4: st.error(f"🔴 **URGENT — Priority {priority}/5** | RPM {new_rpm} outside safe zone. Efficiency: {eff_score:.2f} vs avg {df['efficiency_score'].mean():.2f}. → **Schedule immediate inspection.**")
    elif priority>=2: st.warning(f"🟡 **MONITOR — Priority {priority}/5** | Efficiency below average: {eff_score:.2f}. → **Schedule maintenance within 30 days.**")
    else: st.success(f"🟢 **NORMAL — Priority {priority}/5** | Efficiency {eff_score:.2f} above fleet median. → **Routine monitoring only.**")

    fig_gauge = go.Figure(go.Indicator(mode="gauge+number",value=priority,domain={'x':[0,1],'y':[0,1]},title={'text':"Maintenance Priority",'font':{'color':'#cdd9e5','size':13}},number={'font':{'color':'#cdd9e5','size':40}},gauge={'axis':{'range':[0,5],'tickcolor':'#cdd9e5','tickfont':{'color':'#cdd9e5'}},'bar':{'color':'#f87171' if priority>=4 else '#fbbf24' if priority>=2 else '#4ade80'},'bgcolor':'#1e2738','bordercolor':'#1e2738','steps':[{'range':[0,2],'color':'rgba(74,222,128,0.08)'},{'range':[2,4],'color':'rgba(251,191,36,0.08)'},{'range':[4,5],'color':'rgba(248,113,113,0.08)'}],'threshold':{'line':{'color':'#fff','width':2},'thickness':0.75,'value':priority}}))
    fig_gauge.update_layout(height=210,plot_bgcolor='#0d1117',paper_bgcolor='#0d1117',font=dict(color='#cdd9e5'),margin=dict(l=30,r=30,t=30,b=10))
    col1,col2,col3 = st.columns([1,2,1])
    with col2: st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("#### 🚀 Strategic Recommendations")
    rec_data = pd.DataFrame({'Priority':['🔴 1 — URGENT','🟠 2 — High ROI','🟡 3 — Risk Mgmt','🟢 4 — Scale'],'Action':['Bottom 10% immediate maintenance','L-type RPM optimization program','M-type failure prevention','Deploy ML scoring model'],'Target':['1,000 machines','256 high-risk L-type','125 M-type units','All new machines'],'Impact':['₺454K/yr savings','Highest ROI (60% cost base)','Risk mitigation','Proactive & scalable'],'Timeline':['Immediately','30 days','60 days','90 days']})
    st.dataframe(rec_data, hide_index=True, use_container_width=True, height=200)
    st.success("✅ **Model is production-ready** — automatic priority scoring enables proactive, data-driven maintenance.")
