import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="Üretim Analizi | N. Nur Altay",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SESSION STATE (NAVIGASYON) ---
if 'page' not in st.session_state:
    st.session_state.page = 'Kapak'

def nav_to(page_name):
    st.session_state.page = page_name

# --- 3. CUSTOM CSS (TASARIM SİSTEMİ) ---
st.markdown("""
<style>
    /* Ana Tema Ayarları */
    .stApp { background-color: #07090f; color: #cdd9e5; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Navigasyon Butonları Tasarımı */
    .stButton > button {
        width: 100%; border-radius: 8px; border: 1px solid #1e2738;
        background-color: #0d1117; color: #4a6072; font-weight: bold;
        transition: 0.3s all;
    }
    .stButton > button:hover { border-color: #38bdf8; color: #38bdf8; }
    
    /* KPI Kartları */
    .kpi-card {
        background: #0d1117; border: 1px solid #1e2738; border-radius: 12px;
        padding: 20px; text-align: left; border-top: 3px solid #38bdf8;
    }
    .kpi-label { font-size: 10px; color: #4a6072; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-val { font-size: 28px; font-weight: 800; color: #fff; font-family: 'monospace'; }
    
    /* Kart Yapıları */
    .main-card { background: #0d1117; border: 1px solid #1e2738; border-radius: 12px; padding: 20px; }
    .insight-box { background: rgba(56, 189, 248, 0.05); border-left: 3px solid #38bdf8; padding: 15px; border-radius: 4px; margin: 15px 0; font-size: 13px; }
    
    /* Tablo Tasarımı */
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; }
    .custom-table th { color: #4a6072; text-align: left; padding: 10px; border-bottom: 1px solid #1e2738; }
    .custom-table td { padding: 10px; border-bottom: 1px solid #1e2738; }
</style>
""", unsafe_allow_html=True)

# --- 4. ÜST NAVİGASYON BARI ---
nav_cols = st.columns([2, 1, 1, 1, 1, 1, 2])
with nav_cols[1]: st.button("🏠 KAPAK", on_click=nav_to, args=('Kapak',))
with nav_cols[2]: st.button("📊 GENEL", on_click=nav_to, args=('Genel Bakış',))
with nav_cols[3]: st.button("🔧 ANALİZ", on_click=nav_to, args=('Analiz',))
with nav_cols[4]: st.button("🗄️ SQL", on_click=nav_to, args=('SQL',))
with nav_cols[5]: st.button("🤖 ML MODEL", on_click=nav_to, args=('Model',))

st.markdown("---")

# --- 5. SAYFA İÇERİKLERİ ---

# --- A. KAPAK SAYFASI ---
if st.session_state.page == 'Kapak':
    st.write("")
    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"""
            <div style="text-align: center; padding: 50px;">
                <div style="font-size: 100px;">⚡</div>
                <h1 style="font-size: 50px; background: linear-gradient(135deg, #38bdf8, #4ade80); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Üretim Enerji Verimliliği &<br>Kestirimci Bakım Analizi
                </h1>
                <p style="color: #4a6072; font-size: 20px; margin-top: 20px;">10,000 Makine Kaydı Üzerinden Veri Odaklı Karar Destek Sistemi</p>
                <div style="margin: 40px auto; width: 60px; height: 3px; background: #38bdf8;"></div>
                <p style="font-size: 16px;">Hazırlayan: <b>N. Nur Altay</b></p>
                <p style="color: #4a6072; font-size: 12px;">Endüstri 4.0 Analitiği | Python | SQL | Machine Learning</p>
            </div>
        """, unsafe_allow_html=True)

# --- B. GENEL BAKIŞ ---
elif st.session_state.page == 'Genel Bakış':
    # KPI Row
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown('<div class="kpi-card"><div class="kpi-label">Toplam Makine</div><div class="kpi-val">10.000</div></div>', unsafe_allow_html=True)
    k2.markdown('<div class="kpi-card" style="border-top-color:#f87171"><div class="kpi-label">Yüksek Riskli</div><div class="kpi-val" style="color:#f87171">418</div></div>', unsafe_allow_html=True)
    k3.markdown('<div class="kpi-card" style="border-top-color:#4ade80"><div class="kpi-label">Verimlilik</div><div class="kpi-val" style="color:#4ade80">%38.45</div></div>', unsafe_allow_html=True)
    k4.markdown('<div class="kpi-card" style="border-top-color:#fb923c"><div class="kpi-label">Maliyet (S)</div><div class="kpi-val" style="color:#fb923c">1.24 TL</div></div>', unsafe_allow_html=True)
    k5.markdown('<div class="kpi-card" style="border-top-color:#a78bfa"><div class="kpi-label">Arıza Kaydı</div><div class="kpi-val" style="color:#a78bfa">348</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="insight-box">💡 <b>Temel Bulgu:</b> Yüksek riskli makineler, normal çalışma moduna göre <b>%27.8 daha verimsiz</b> skorlara sahip.</div>', unsafe_allow_html=True)

    g1, g2 = st.columns([2, 1])
    with g1:
        st.markdown('<div class="main-card"><b>RPM Dağılımı — Normal vs Yüksek Riskli</b>', unsafe_allow_html=True)
        # Plotly Histogram
        df_hist = pd.DataFrame({'RPM': [1200, 1400, 1600, 1800, 2000, 2500], 'Normal': [500, 2800, 2500, 1500, 800, 200], 'Riskli': [50, 20, 10, 5, 120, 150]})
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_hist['RPM'], y=df_hist['Normal'], name='Normal', marker_color='#38bdf8'))
        fig.add_trace(go.Bar(x=df_hist['RPM'], y=df_hist['Riskli'], name='Riskli', marker_color='#f87171'))
        fig.update_layout(barmode='group', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g2:
        st.markdown('<div class="main-card"><b>Arıza Tipi Dağılımı</b>', unsafe_allow_html=True)
        fig_pie = px.pie(values=[9652, 112, 95, 78, 45], names=['Yok', 'Isı', 'Güç', 'Aşırı Yük', 'Takım'], hole=0.6)
        fig_pie.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=300, margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- C. ANALİZ ---
elif st.session_state.page == 'Analiz':
    st.markdown('<div class="main-card"><b>Makine Tipi × Özellik Isı Haritası</b>', unsafe_allow_html=True)
    # Heatmap verisi
    hm_data = [[1552, 41.5, 108, 10], [1542, 40.0, 107, 10], [1532, 39.8, 108, 9]]
    fig_hm = px.imshow(hm_data, labels=dict(x="Özellik", y="Tip", color="Yoğunluk"),
                x=['RPM', 'Tork', 'Tool Wear', 'Sıcaklık'], y=['L-Tipi', 'M-Tipi', 'H-Tipi'], text_auto=True, color_continuous_scale='Viridis')
    fig_hm.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig_hm, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown('<div class="main-card" style="margin-top:20px;"><b>Vardiya Dağılımı</b>', unsafe_allow_html=True)
        st.bar_chart({'Vardiya': ['Gece', 'Gündüz', 'Pik'], 'Makine': [1157, 7788, 1055]})
        st.markdown('</div>', unsafe_allow_html=True)
    with col_a2:
        st.markdown('<div class="main-card" style="margin-top:20px;"><b>Enerji Kategorisi</b>', unsafe_allow_html=True)
        st.write("Yüksek Riskli makinelerin %97.6'sı düşük tork nedeniyle 'Low' kategorisindedir.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- D. SQL SORGULARI ---
elif st.session_state.page == 'SQL':
    st.subheader("🗄️ Veritabanı Analiz Sonuçları")
    c_sql1, c_sql2 = st.columns(2)
    with c_sql1:
        st.markdown("""<div class="main-card"><b>Query 1: Tip Bazlı Maliyet</b><pre style="color:#fb923c">SELECT Type, SUM(annual_cost) FROM machines GROUP BY Type</pre>
        <table class="custom-table"><tr><th>Tip</th><th>Adet</th><th>Yıllık Maliyet</th></tr><tr><td>L</td><td>6000</td><td>65.5M TL</td></tr><tr><td>M</td><td>2997</td><td>32.7M TL</td></tr></table></div>""", unsafe_allow_html=True)
    with c_sql2:
        st.markdown("""<div class="main-card"><b>Query 3: Arıza Riski</b><pre style="color:#fb923c">SELECT Type, AVG(Target) FROM machines WHERE risk=1</pre>
        <table class="custom-table"><tr><th>Tip</th><th>Adet</th><th>Arıza Oranı</th></tr><tr><td>M</td><td>125</td><td>%9.6</td></tr><tr><td>L</td><td>256</td><td>%8.6</td></tr></table></div>""", unsafe_allow_html=True)

# --- E. ML MODELİ ---
elif st.session_state.page == 'Model':
    # Metrik Satırı
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown('<div class="kpi-card" style="border-top-color:#4ade80"><div class="kpi-label">Doğruluk</div><div class="kpi-val" style="color:#4ade80">100%</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="kpi-card" style="border-top-color:#38bdf8"><div class="kpi-label">Özellik Sayısı</div><div class="kpi-val" style="color:#38bdf8">7</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="kpi-card" style="border-top-color:#fb923c"><div class="kpi-label">Ağaç Sayısı</div><div class="kpi-val" style="color:#fb923c">100</div></div>', unsafe_allow_html=True)
    m4.markdown('<div class="kpi-card" style="border-top-color:#a78bfa"><div class="kpi-label">Split</div><div class="kpi-val" style="color:#a78bfa">80/20</div></div>', unsafe_allow_html=True)

    col_ml1, col_ml2 = st.columns(2)
    with col_ml1:
        st.markdown('<div class="main-card" style="margin-top:20px;"><b>Yeni Makine Tahmin Simülatörü</b>', unsafe_allow_html=True)
        s_rpm = st.slider("RPM Değeri", 1000, 3000, 2500)
        s_eff = st.slider("Verimlilik Skoru (%)", 0, 100, 15)
        
        # Basit AI Karar Mantığı
        res_val = "4" if s_rpm > 2200 and s_eff < 20 else "0"
        res_col = "#f87171" if res_val == "4" else "#4ade80"
        
        st.markdown(f"""<div style="text-align:center; padding:20px; background:rgba(255,255,255,0.05); border-radius:10px;">
        <div style="color:#4a6072; font-size:12px;">TAHMİN EDİLEN ÖNCELİK</div>
        <div style="font-size:60px; font-weight:900; color:{res_col}">{res_val}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_ml2:
        st.markdown('<div class="main-card" style="margin-top:20px;"><b>Özellik Önem Sıralaması</b>', unsafe_allow_html=True)
        fig_imp = px.bar(x=[0.42, 0.28, 0.12, 0.08, 0.05], y=['RPM', 'Verimlilik', 'Tork', 'Güç', 'Aşınma'], orientation='h', color_discrete_sequence=['#38bdf8'])
        fig_imp.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_imp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
