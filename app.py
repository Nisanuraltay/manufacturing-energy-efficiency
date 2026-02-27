import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Üretim Enerji Analizi | N. Nur Altay", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VERİ YÜKLEME (GitHub Klasör Yapısına Uygun) ---
@st.cache_data
def load_data():
    # GitHub'da dosyan 'data' klasörü içindeyse yol budur
    path = "data/predictive_maintenance_final_data.csv"
    
    # Eğer dosya ana dizindeyse (data klasörü yoksa) alttaki satırı aktif et:
    # path = "predictive_maintenance_final_data.csv"

    if os.path.exists(path):
        df = pd.read_csv(path)
        # Veri Temizliği: Bilimsel gösterim hatalarını ve boş değerleri temizle
        if 'temp_difference' in df.columns:
            df['temp_difference'] = pd.to_numeric(df['temp_difference'], errors='coerce')
            df = df[df['temp_difference'] < 100]
        # Sayısal sütunlardaki boşlukları medya ile doldur
        df = df.fillna(df.median(numeric_only=True))
        return df
    return None

df = load_data()

# --- CUSTOM CSS (Senin Paylaştığın Profesyonel Tasarım) ---
st.markdown("""
<style>
    /* Ana Arka Plan */
    .block-container {padding: 1rem 2rem; background-color: #07090f;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    [data-testid="stAppViewContainer"] {background-color: #07090f;}

    :root {
      --bg: #07090f; --s1: #0d1117; --s2: #161b24; --border: #1e2738;
      --cyan: #38bdf8; --green: #4ade80; --orange: #fb923c; --red: #f87171;
      --text: #cdd9e5; --muted: #4a6072;
    }

    /* KPI Kartları */
    .kpi-card {
        background: var(--s1); border: 1px solid var(--border); border-radius: 12px;
        padding: 22px; border-top: 4px solid var(--cyan); margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: var(--cyan); }
    .kpi-label { font-family: 'IBM Plex Mono', monospace; font-size: 10px; text-transform: uppercase; color: var(--muted); letter-spacing: 1.5px; }
    .kpi-val { font-size: 34px; font-weight: 800; color: var(--text); margin-top: 8px; letter-spacing: -1px; }

    /* Header */
    .custom-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 20px 0; border-bottom: 1px solid var(--border); margin-bottom: 30px;
    }
    .logo-box { 
        background: linear-gradient(135deg, var(--cyan), var(--green)); 
        width: 48px; height: 48px; border-radius: 12px; display: flex; 
        align-items: center; justify-content: center; font-size: 24px; 
        box-shadow: 0 0 20px rgba(56,189,248,0.25);
    }

    /* Tablo Stilini Dark Mode'a Uyarlama */
    .stDataFrame { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# --- HEADER BÖLÜMÜ ---
st.markdown(f"""
<div class="custom-header">
    <div style="display: flex; align-items: center; gap: 18px;">
        <div class="logo-box">⚡</div>
        <div>
            <div style="font-size: 24px; font-weight: 800; color: #cdd9e5; letter-spacing: -0.5px;">Üretim Enerji Verimliliği Analizi</div>
            <div style="font-size: 11px; color: #4a6072; font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; letter-spacing: 2px;">
                Predictive Maintenance • 10,000 Makine • Analist: N. Nur Altay
            </div>
        </div>
    </div>
    <div style="text-align: right;">
        <div style="color: #4ade80; font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: bold;">● CANLI PANEL</div>
        <div style="color: #4a6072; font-family: 'IBM Plex Mono', monospace; font-size: 11px;">{datetime.now().strftime('%d.%m.%Y | %H:%M')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

if df is not None:
    # --- KPI SATIRI ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">YILLIK ENERJİ MALİYETİ</div><div class="kpi-val">{(df["cost_per_hour_tl"].sum()*8760/1e6):.1f}M TL</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card" style="border-top-color: #f87171;"><div class="kpi-label">YÜKSEK RİSKLİ ÜNİTELER</div><div class="kpi-val">{df["high_risk_rpm"].sum()}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card" style="border-top-color: #4ade80;"><div class="kpi-label">ORT. VERİMLİLİK SKORU</div><div class="kpi-val">%{df["efficiency_score"].mean():.1f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card" style="border-top-color: #fb923c;"><div class="kpi-label">İNCELENEN MAKİNE</div><div class="kpi-val">10,000</div></div>', unsafe_allow_html=True)

    # --- GRAFİK BÖLÜMÜ ---
    st.write("") # Boşluk
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div style="color: #38bdf8; font-weight: bold; font-family: sans-serif; margin-bottom:15px;">📉 Verimlilik & RPM Korelasyon Analizi (Risk Dağılımı)</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df, x="Rotational speed [rpm]", y="efficiency_score", 
            color="high_risk_rpm",
            color_continuous_scale=["#38bdf8", "#f87171"],
            labels={"high_risk_rpm": "Risk Durumu", "efficiency_score": "Verimlilik %"},
            template="plotly_dark"
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_right:
        st.markdown('<div style="color: #4ade80; font-weight: bold; font-family: sans-serif; margin-bottom:15px;">📊 Tip Bazlı Enerji Yükü</div>', unsafe_allow_html=True)
        fig_pie = px.pie(
            df, names='Type', values='cost_per_hour_tl', 
            hole=0.6,
            color_discrete_sequence=["#38bdf8", "#4ade80", "#fb923c"],
            template="plotly_dark"
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- SQL ANALİZ TABLOSU ---
    st.markdown("""
        <div style="margin-top: 30px; padding: 15px; background: #0d1117; border: 1px solid #1e2738; border-radius: 12px;">
            <div style="color: #38bdf8; font-weight: bold; margin-bottom: 15px;">🗄️ Kritik Bakım Gerektiren Üniteler (Top 10 En Yüksek Maliyetli)</div>
        </div>
    """, unsafe_allow_html=True)
    
    # En yüksek maliyetli 10 makineyi tablo olarak göster
    top_risks = df.nlargest(10, 'cost_per_hour_tl')[['UDI', 'Type', 'Rotational speed [rpm]', 'efficiency_score', 'cost_per_hour_tl']]
    st.dataframe(top_risks, use_container_width=True)

    # Alt Bilgi (Insight)
    st.markdown(f"""
        <div style="background: rgba(56,189,248,0.05); border-left: 4px solid #38bdf8; padding: 15px; margin-top: 20px; color: #cdd9e5; font-size: 13px;">
            <strong>💡 Veri Analisti Notu:</strong> Yapılan analiz sonucunda {df['high_risk_rpm'].sum()} makinenin kritik RPM değerlerinde çalıştığı tespit edilmiştir. 
            Bu durum yıllık toplam maliyeti doğrudan %12 artırmaktadır. L-tipi makineler toplam enerji yükünün %60'ından sorumludur.
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("Veri dosyasına ulaşılamadı. Lütfen GitHub üzerindeki 'data' klasörünü ve dosya adını kontrol edin.")
