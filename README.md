⚡ Manufacturing Energy Efficiency Analysis
🎯 Proje Özeti
Bir üretim tesisindeki 10,000 makine saatlik verisi kullanılarak enerji verimliliği optimizasyonu ve maliyet tasarrufu fırsatları tespit edilmiştir.
Ana Bulgu: 418 makine (%4.18) verimsiz çalışmakta ve yıllık 227,000 TL optimizasyon potansiyeli bulunmaktadır.

💼 İş Problemi
Üretim tesisinde:

300 makine 7/24 çalışıyor
Aylık elektrik maliyeti ~50,000 TL
Hedef: %10-15 enerji tasarrufu sağlamak

Potansiyel Değer: 60,000 - 90,000 TL/yıl tasarruf

📊 Veri Seti
Kaynak: Kaggle - Machine Predictive Maintenance Classification

Boyut: 10,000 satır × 10 kolon
İçerik: Makine sensör verileri (sıcaklık, RPM, tork, aşınma)
Yeniden Çerçeveleme: Arıza tahmini → Enerji verimliliği analizi


🔍 Temel Bulgular
1. High-Risk Makine Tespiti

418 makine (%4.18) anormal çalışma profili gösteriyor
Ortalama RPM: 2102 (normal: 1514) → %39 daha hızlı
Ortalama Tork: 18.9 Nm (normal: 40.9) → %54 daha düşük

2. Verimsizlik Kanıtı

Yüksek hız + düşük tork = boşa enerji harcama
Arıza oranı: %8.37 (normal: %3.17) → 2.6 kat fazla!

3. İş Etkisi

High-risk makineler yıllık 454,826 TL arıza maliyeti oluşturuyor
Optimizasyon potansiyeli: ~227,000 TL/yıl

4. Öncelik Analizi

L tipi makineler: 256 adet (%61) → En yüksek öncelik
M tipi makineler: 125 adet (%30)
H tipi makineler: 37 adet (%9)


📂 Proje Yapısı
manufacturing-energy-efficiency/
│
├── data/
│   ├── raw/                          # Ham veri
│   └── processed/                    # İşlenmiş veri
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    ✅ Tamamlandı
│   ├── 02_feature_engineering.ipynb  🔄 Devam ediyor
│   ├── 03_modeling.ipynb             ⏳ Beklemede
│   └── 04_sql_analysis.ipynb         ⏳ Beklemede
│
├── sql/
│   └── energy_analysis_queries.sql
│
├── dashboards/
│   └── energy_dashboard.pbix
│
├── reports/
│   └── optimization_recommendations.pdf
│
├── images/                           # Görsel materyaller
│
├── .gitignore
├── README.md
└── requirements.txt

📓 Analiz Süreci
✅ Tamamlanan Aşamalar
1. Keşifsel Veri Analizi (EDA)

10,000 makine verisi analiz edildi
Veri kalitesi kontrolü (tip düzeltme, duplicate kontrolü)
Outlier analizi (IQR yöntemi) - 418 high-risk makine tespit edildi
Hipotez testi: "Hafif iş" hipotezi test edildi ve çürütüldü
İş değeri: 227K TL/yıl optimizasyon potansiyeli hesaplandı

Metodoloji:

✅ Outlier'lar silinmedi, etiketlendi (best practice)
✅ Hipotez testi yapıldı (veri odaklı karar)
✅ Domain knowledge ile formüller yorumlandı
✅ İş değeri odaklı analiz

📓 Notebook: 01_data_exploration.ipynb

🔜 Devam Eden Çalışmalar
2. Feature Engineering

Enerji tüketimi metrikleri (kW, maliyet/saat)
Verimlilik skorları
Vardiya simülasyonu (gece/gündüz tarife farkları)

3. SQL Analizi

Maliyet segmentasyonu (tip/vardiya bazlı)
En verimsiz %10 makinelerin tespiti
Optimizasyon önceliklendirme

4. Tahmin Modeli

"Hangi makine optimize edilmeli?" tahmin modeli
Feature importance analizi
Risk skorlaması

5. Power BI Dashboard

Yönetici özet raporu
Makine performans takibi
Optimizasyon önerileri (interaktif)


🛠️ Kullanılan Teknolojiler
Analiz & Modelleme:

Python 3.x
Pandas, NumPy (veri manipülasyonu)
Matplotlib, Seaborn, Plotly (görselleştirme)
Scikit-learn (makine öğrenmesi)

Veritabanı:

SQLite (lokal analiz)
SQL (maliyet segmentasyonu)

Raporlama:

Power BI (interaktif dashboard)
Jupyter Notebook (teknik dokümantasyon)

Versiyon Kontrol:

Git & GitHub


🚀 Nasıl Çalıştırılır?
1. Repository'yi Klonla
bashgit clone https://github.com/Nisanuraltay/manufacturing-energy-efficiency.git
cd manufacturing-energy-efficiency
2. Gerekli Kütüphaneleri Yükle
bashpip install -r requirements.txt
3. Notebook'ları Çalıştır
bashjupyter notebook
Not: Veri seti data/raw/ klasörüne Kaggle'dan indirilmelidir.

📌 Proje Hedefleri
Bu proje, kariyer değişikliği sürecinde veri analizi yetkinliklerimi göstermek için geliştirilmiştir.
Odak alanlar:

✅ Gerçek iş problemlerini çözme
✅ Veri odaklı karar verme
✅ İş değeri hesaplama (TL/yıl)
✅ Profesyonel raporlama
✅ End-to-end proje yönetimi


📊 Sonraki Adımlar

⏳ Feature engineering ve enerji metrikleri
⏳ SQL ile derinlemesine maliyet analizi
⏳ Machine learning modeli (optimizasyon önceliklendirme)
⏳ Power BI dashboard geliştirme
⏳ Yönetici raporu hazırlama


👤 İletişim
Proje Sahibi: Nisa Nur Altay
GitHub: github.com/Nisanuraltay
LinkedIn: linkedin.com/in/nisanuraltay 

⭐ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın!
