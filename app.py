import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── SAYFA AYARLARI ──
st.set_page_config(
    page_title="Energy Efficiency AI | N.Nur Altay",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .hero-text {
        font-size: 42px; font-weight: 700;
        background: linear-gradient(135deg, #38bdf8, #4ade80);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-top: 20px; line-height: 1.2;
    }
    .sub-text {
        font-size: 17px; text-align: center; color: #64748b;
        margin-bottom: 32px; margin-top: 8px;
    }
    .project-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 28px; border-radius: 16px;
        border: 1px solid #1e3a5f;
        border-left: 4px solid #38bdf8;
        color: #cbd5e1;
    }
    .project-card h3 { color: #38bdf8; margin-bottom: 12px; }
    .project-card ul { padding-left: 20px; line-height: 2; }
    .project-card b { color: #e2e8f0; }
    .insight-box {
        background: linear-gradient(135deg, rgba(56,189,248,0.08), rgba(74,222,128,0.05));
        border: 1px solid rgba(56,189,248,0.2);
        border-radius: 10px; padding: 14px 18px;
        font-size: 14px; color: #94a3b8; margin: 12px 0;
    }
    .insight-box b { color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# ── VERİ YÜKLEME ──
@st.cache_data
def load_data():
    # GitHub repo'da data/ klasöründe olacak
    df = pd.read_csv("data/predictive_maintenance_final_data.csv")
    if 'temp_difference' in df.columns:
        df['temp_difference'] = pd.to_numeric(df['temp_difference'], errors='coerce')
        df = df[df['temp_difference'] < 100]
    return df

try:
    df = load_data()
    data_loaded = True
except Exception as e:
    data_loaded = False
    st.error(f"Veri yüklenemedi: {e}")

# ── SIDEBAR ──
st.sidebar.image("https://img.icons8.com/fluency/96/lightning-bolt.png", width=60)
st.sidebar.markdown("## ⚡ Energy Efficiency AI")
st.sidebar.markdown("**Analyst:** N.Nur Altay")
st.sidebar.markdown("**Dataset:** 10,000 Machines")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate:",
    ["🏠 Overview", "📈 Executive Summary", "🔧 Machine Analysis", "🤖 Predictive AI"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Tech Stack:**
- 🐍 Python (Pandas, Sklearn)
- 🗄️ SQLite (3 Queries)
- 🤖 Random Forest (100% Acc)
- 📊 Streamlit + Plotly
""")
st.sidebar.markdown("[📁 GitHub Repo](https://github.com)")

# ══════════════════════════════════════════
# 1. OVERVIEW / KAPAK SAYFASI
# ══════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown('<p class="hero-text">Industrial Energy Efficiency<br>& Predictive Maintenance AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">End-to-end Data Analysis · 10,000 Machines · $90K Annual Savings Potential</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>📌 Project Overview</h3>
            <p>End-to-end data solution to reduce energy waste in industrial machinery through sensor data analysis.</p>
            <ul>
                <li><b>EDA:</b> 418 high-risk machines identified (IQR method, 4.18%)</li>
                <li><b>Feature Engineering:</b> 6 custom metrics (efficiency, cost, priority)</li>
                <li><b>SQL:</b> 3 business queries — type cost, bottom 10%, risk segment</li>
                <li><b>ML Model:</b> Random Forest — 100% accuracy on priority prediction</li>
                <li><b>Business Value:</b> ~2.96M TL annual cost impact identified</li>
            </ul>
            <hr style="border-color:#1e3a5f; margin:16px 0">
            <p><b>Author:</b> N.Nur Altay &nbsp;|&nbsp; <b>Tools:</b> Python, SQL, Scikit-learn, Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI BAR
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🏭 Total Machines", "10,000")
    c2.metric("⚠️ High-Risk Units", "418", delta="-4.18% fleet")
    c3.metric("📈 Avg Efficiency", "38.45", delta="Normal machines")
    c4.metric("📉 Risk Efficiency", "27.76", delta="-27.8% vs normal", delta_color="inverse")
    c5.metric("💰 Savings Potential", "$90K/yr")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="insight-box">💡 <b>Key Finding:</b> High-risk machines operate at high RPM (avg 2,102) with low torque (avg 18.9 Nm), creating a <b>27.8% efficiency gap</b> compared to normal machines. L-type machines account for <b>60% of total energy costs</b>.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# 2. EXECUTIVE SUMMARY
# ══════════════════════════════════════════
elif page == "📈 Executive Summary":
    st.title("📈 Executive Energy Overview")

    if data_loaded:
        c1, c2, c3, c4 = st.columns(4)
        total_cost_m = (df['cost_per_hour_tl'].sum() * 8760) / 1_000_000
        c1.metric("Annual Energy Cost", f"{total_cost_m:.1f}M TL")
        c2.metric("Analyzed Machines", f"{len(df):,}")
        c3.metric("High-Risk Units", f"{int(df['high_risk_rpm'].sum())}")
        c4.metric("Avg Hourly Cost", f"{df['cost_per_hour_tl'].mean():.2f} TL/h")

        st.markdown("---")

        col_a, col_b = st.columns(2)
        with col_a:
            fig1 = px.pie(
                df, names='Type', values='cost_per_hour_tl', hole=0.55,
                title="💰 Cost Distribution by Machine Type",
                color_discrete_sequence=['#38bdf8', '#4ade80', '#fb923c']
            )
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            fig2 = px.scatter(
                df, x="efficiency_score", y="cost_per_hour_tl",
                color="Type", title="📊 Efficiency vs. Operating Cost",
                color_discrete_sequence=['#38bdf8', '#4ade80', '#fb923c'],
                opacity=0.6
            )
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        col_c, col_d = st.columns(2)
        with col_c:
            fig3 = px.histogram(
                df, x="efficiency_score", color="high_risk_rpm",
                title="📈 Efficiency Score Distribution",
                barmode="overlay",
                color_discrete_map={0: '#4ade80', 1: '#f87171'},
                labels={"high_risk_rpm": "Risk", "efficiency_score": "Efficiency Score"}
            )
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3, use_container_width=True)

        with col_d:
            prio_counts = df['optimization_priority'].value_counts().sort_index().reset_index()
            prio_counts.columns = ['Priority', 'Count']
            colors = ['#4ade80','#4ade80','#fbbf24','#fbbf24','#f87171','#f87171']
            fig4 = px.bar(prio_counts, x='Priority', y='Count',
                title="🎯 Optimization Priority Distribution",
                color='Priority', color_discrete_sequence=colors)
            fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown('<div class="insight-box">💡 <b>SQL Finding:</b> L-type machines = 60% of annual cost (65.5M TL). M-type has highest failure rate at 9.6%. Immediate action on bottom 10% (1,000 machines) recommended.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# 3. MACHINE ANALYSIS
# ══════════════════════════════════════════
elif page == "🔧 Machine Analysis":
    st.title("🔧 Machine-Level Analysis")

    if data_loaded:
        st.subheader("High-Risk Machine Segmentation")
        seg_data = pd.DataFrame({
            'Type': ['L-Type', 'M-Type', 'H-Type'],
            'Count': [256, 125, 37],
            'Avg_RPM': [2103, 2098, 2109],
            'Avg_Efficiency': [27.76, 27.79, 27.62],
            'Failure_Rate': [8.6, 9.6, 2.7],
            'Annual_Cost_TL': [1817431, 884486, 258766]
        })
        st.dataframe(seg_data, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(seg_data, x='Type', y='Count',
                title="High-Risk Machine Count by Type",
                color='Failure_Rate', color_continuous_scale='RdYlGn_r',
                labels={'Count': 'Machine Count', 'Failure_Rate': 'Failure %'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.scatter(
                df, x="Rotational speed [rpm]", y="efficiency_score",
                color=df['high_risk_rpm'].map({0: 'Normal', 1: 'High-Risk'}),
                title="RPM vs Efficiency — Risk Segmentation",
                color_discrete_map={'Normal': '#4ade80', 'High-Risk': '#f87171'},
                opacity=0.5
            )
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("📊 Failure Type Analysis")
        failure_counts = df['Failure Type'].value_counts().reset_index()
        failure_counts.columns = ['Failure Type', 'Count']
        fig3 = px.bar(failure_counts, x='Count', y='Failure Type', orientation='h',
            title="Failure Distribution (348 total failures)",
            color='Count', color_continuous_scale='reds')
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('<div class="insight-box">💡 <b>Priority Order:</b> <b>L-type</b> (volume: 256 units) → <b>M-type</b> (risk: 9.6% failure) → H-type (low risk: 2.7%). All high-risk machines operate in night shift (low torque = misleading low power formula).</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════
# 4. PREDICTIVE AI
# ══════════════════════════════════════════
elif page == "🤖 Predictive AI":
    st.title("🤖 Predictive AI Analysis")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Model Accuracy", "100%", delta="Random Forest")
    m2.metric("Precision", "100%")
    m3.metric("Recall", "100%")
    m4.metric("F1-Score", "100%")

    st.markdown("---")

    col_x, col_y = st.columns(2)
    with col_x:
        importance = pd.DataFrame({
            'Feature': ['RPM', 'Efficiency Score', 'Torque', 'Power (kW)', 'Failure Status', 'Tool Wear', 'Temp Diff'],
            'Importance': [0.42, 0.28, 0.12, 0.08, 0.05, 0.03, 0.02]
        })
        fig_fi = px.bar(importance, x='Importance', y='Feature', orientation='h',
            title="🔍 Feature Importance — Which Factors Drive Priority?",
            color='Importance', color_continuous_scale='blues')
        fig_fi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_y:
        if data_loaded:
            fig_rpm = px.histogram(
                df, x="Rotational speed [rpm]",
                color=df['high_risk_rpm'].map({0: 'Normal', 1: 'High-Risk'}),
                title="📊 RPM Risk Distribution",
                barmode="overlay",
                color_discrete_map={'Normal': '#38bdf8', 'High-Risk': '#f87171'}
            )
            fig_rpm.add_vline(x=1895, line_dash="dash", line_color="#fbbf24",
                             annotation_text="Upper Bound (1895 RPM)")
            fig_rpm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_rpm, use_container_width=True)

    st.markdown("---")
    st.subheader("🔮 New Machine Prediction Simulator")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        new_rpm = st.slider("Rotational Speed (RPM)", 1168, 2886, 2500)
    with col_s2:
        new_torque = st.slider("Torque (Nm)", 3, 76, 12)
    with col_s3:
        new_wear = st.slider("Tool Wear (min)", 0, 253, 180)

    # Simple rule-based prediction (mirrors the model logic)
    eff_score = new_torque / ((new_rpm / 1000) * (new_torque / 100) * 1.73)
    is_high_risk = 1 if new_rpm > 1895 else 0
    is_low_eff = 1 if eff_score < 38.0 else 0
    priority = min(is_high_risk * 2 + is_low_eff * 2, 5)

    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    col_r1.metric("Efficiency Score", f"{eff_score:.1f}")
    col_r2.metric("High-Risk Status", "YES ⚠️" if is_high_risk else "NO ✅")
    col_r3.metric("Optimization Priority", f"{priority} / 5")
    
    if priority >= 4:
        col_r4.metric("Action Required", "🔴 URGENT")
        st.error(f"⚠️ **URGENT MAINTENANCE REQUIRED** — Priority {priority}/5. This machine shows high-risk RPM pattern.")
    elif priority >= 2:
        col_r4.metric("Action Required", "🟡 MONITOR")
        st.warning(f"📊 **Monitor this machine** — Priority {priority}/5. Below average efficiency detected.")
    else:
        col_r4.metric("Action Required", "🟢 NORMAL")
        st.success(f"✅ **Machine operating normally** — Priority {priority}/5.")

    st.markdown('<div class="insight-box">💡 <b>Model Note:</b> Random Forest achieved 100% accuracy because <b>optimization_priority</b> was mathematically derived from the same features used for prediction. For production deployment, use on machines <b>not in the training set</b> for genuine predictive power.</div>', unsafe_allow_html=True)
