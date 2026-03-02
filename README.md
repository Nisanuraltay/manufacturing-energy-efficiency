# ⚡ Manufacturing Energy Efficiency Analysis

> **End-to-end data analytics project** · EDA → Feature Engineering → SQL → Machine Learning → Interactive Dashboard

[![Streamlit App](https://img.shields.io/badge/Live_Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://nisanuraltay-manufacturing-energy-efficiency.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Notebooks-3-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](notebooks/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📋 Table of Contents

- [Project Story](#-project-story)
- [Business Problem](#-business-problem)
- [Dataset](#-dataset)
- [Key Findings](#-key-findings)
- [Analysis Pipeline](#-analysis-pipeline)
- [Interactive Dashboard](#-interactive-dashboard)
- [Strategic Action Plan](#-strategic-action-plan)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [How to Run](#-how-to-run)
- [Limitations](#-data--model-limitations)
- [Contact](#-contact)

---

## 👋 Project Story

This project began with a simple question: *"What if I reframe a predictive maintenance dataset as an energy efficiency problem?"*

Instead of just building a classifier, I approached this as a consultant would — starting with a business problem, forming hypotheses, testing them with data, and delivering actionable financial recommendations.

### 🔄 My First Hypothesis Was Wrong

I initially assumed high-risk machines (extreme RPM) were doing **"light work"** — low torque seemed to suggest easy loads.

**The data proved otherwise.** Their failure rate was **2.6× higher** than normal machines. High RPM + low torque doesn't mean easy work — it means the machine is spinning fast but producing very little useful output. Energy is lost to friction and heat.

> **Lesson:** Test every assumption with data before drawing conclusions.

### ⚠️ The Energy Formula Was Misleading

A simple mechanical power formula `P = (RPM × Torque × 2π) / 60,000` showed high-risk machines consuming *less* energy on paper. But the formula ignores friction losses (which scale with RPM²), motor inefficiency at high speeds, and idle current draw.

**Decision:** I acknowledged the formula's limitations explicitly and pivoted to **failure cost analysis** — more measurable, more credible, more business-relevant.

---

## 🎯 Business Problem

A manufacturing facility runs **10,000 machines** continuously. The challenge: identify which machines are operating inefficiently, quantify the financial impact, and prioritize interventions.

| Metric | Value |
|--------|-------|
| Fleet Size | 10,000 machines |
| High-Risk Machines Detected | 418 (4.18%) |
| Annual Cost Exposure | ₺2.96M |
| Optimization Potential | ₺227K–7M/year |
| Analysis Method | EDA → Feature Eng → SQL → ML → Dashboard |

---

## 📊 Dataset

**Source:** [Kaggle — Machine Predictive Maintenance Classification](https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification)

| Property | Detail |
|----------|--------|
| Records | 10,000 machine observations |
| Raw Features | 10 columns (temperature, RPM, torque, wear, failure type) |
| Engineered Features | +8 (power, efficiency score, cost/hr, priority score, etc.) |
| Machine Types | L (low), M (medium), H (high) |
| Data Quality | Zero missing values · Zero duplicates |

**Reframing:** The original dataset is designed for binary failure prediction. This project reframes it as an **energy efficiency optimization problem** — identifying which machines waste energy, why, and what to do about it.

---

## 🔍 Key Findings

### 1 · High-Risk Machine Detection

Using **IQR outlier detection** on RPM (safe zone: 1,139–1,895 RPM):

| Group | Count | Avg RPM | Avg Torque | Failure Rate |
|-------|-------|---------|------------|--------------|
| Normal | 9,582 | 1,514 | 40.9 Nm | 3.17% |
| High-Risk | 418 | 2,102 | 18.9 Nm | **8.37%** |
| **Difference** | — | **+39%** | **−54%** | **2.6× higher** |

### 2 · Root Cause: Wrong Operating Point

High-risk machines run at high speed but generate low torque — the worst combination for efficiency:

```
P = (RPM × Torque × 2π) / 60,000
```

High RPM + Low Torque = **energy converted to friction and heat, not useful work.**

Confirmed by the efficiency gap:

| Group | Avg Efficiency Score |
|-------|---------------------|
| Normal | 38.45 |
| High-Risk | 27.76 |
| **Gap** | **−27.8%** |

### 3 · Fleet Cost Segmentation (SQL Analysis)

| Machine Type | High-Risk Units | Failure Rate | Annual Cost |
|--------------|-----------------|--------------|-------------|
| L-Type | 256 (61%) | 8.6% | ₺1,817,431 |
| M-Type | 125 (30%) | **9.6%** | ₺884,486 |
| H-Type | 37 (9%) | 2.7% | ₺258,766 |

> L-type = highest total cost (volume). M-type = highest per-unit failure risk.

### 4 · Machine Learning Results

**Random Forest** predicting optimization priority (0–5):

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest (100 trees, max_depth=10) |
| Accuracy | 100% on test set |
| #1 Feature | RPM (42% importance) |
| Cross-validation | 5-fold |

Feature importance ranking:

| Rank | Feature | Importance |
|------|---------|-----------|
| 1 | Rotational speed (RPM) | 42% |
| 2 | Efficiency score | 28% |
| 3 | Torque | 12% |
| 4 | Power consumption | 8% |
| 5–7 | Failure status, tool wear, temp diff | 10% |

---

## 🔬 Analysis Pipeline

### Notebook 1 · Data Exploration [`01_data_exploration.ipynb`](notebooks/01_data_exploration.ipynb)

**Goal:** Understand the data, detect anomalies, test hypotheses.

- Data type validation and correction
- Duplicate check — zero found
- **IQR outlier detection** on RPM → 418 high-risk machines flagged
- **Hypothesis test:** "High-risk machines do light work" → ❌ Rejected (failure rate 2.6× higher)
- Failure cost estimate: ₺454K/year for high-risk group
- **Key decision:** Label outliers instead of deleting — high RPM may reflect a different but valid operating state

---

### Notebook 2 · Feature Engineering [`02_feature_engineering.ipynb`](notebooks/02_feature_engineering.ipynb)

**Goal:** Build business-meaningful metrics from raw sensor data.

| Feature | Formula / Method | Business Meaning |
|---------|-----------------|------------------|
| `power_consumption_kw` | `(RPM/1000) × (Torque/100) × 1.73` | Estimated mechanical power |
| `calculated_power_kw` | `(RPM × Torque × 2π) / 60,000` | Exact mechanical power |
| `efficiency_score` | `Torque / power_consumption_kw` | Work output per unit of energy |
| `cost_per_hour_tl` | `power_kw × 1.2 TL/kWh` | Hourly electricity cost |
| `shift` | Torque-based proxy | Shift-based cost variation |
| `energy_category` | Low / Medium / High thresholds | Consumption classification |
| `optimization_priority` | Weighted score 0–5 | Maintenance urgency |
| `high_risk_rpm` | IQR flag (0/1) | Anomaly label |

*Note: The simplified power formula captures mechanical output only. Friction losses, motor inefficiency, and idle draw are not included. This is documented explicitly; the efficiency score and failure rate serve as primary business metrics.*

---

### Notebook 3 · SQL Analysis & Modeling [`03_sql_modeling.ipynb`](notebooks/03_sql_modeling.ipynb)

**Goal:** Answer three business questions with SQL, then build a deployable scoring model.

**SQL queries (SQLite on 10,000 records):**

```sql
-- Query 1: Annual energy cost by machine type
SELECT Type, COUNT(*) AS machines,
       ROUND(AVG(efficiency_score), 2) AS avg_efficiency,
       ROUND(SUM(cost_per_hour_tl) * 24 * 365, 0) AS annual_cost_tl
FROM machines GROUP BY Type ORDER BY annual_cost_tl DESC;

-- Query 2: Bottom 10% — least efficient machines
SELECT UDI, Type, "Rotational speed [rpm]" AS RPM,
       efficiency_score, optimization_priority
FROM machines
ORDER BY efficiency_score ASC
LIMIT (SELECT COUNT(*) * 0.1 FROM machines);

-- Query 3: High-risk segmentation by type
SELECT Type, COUNT(*) AS count,
       ROUND(AVG("Rotational speed [rpm]"), 0) AS avg_rpm,
       ROUND(AVG(Target) * 100, 1) AS failure_rate_pct,
       ROUND(SUM(cost_per_hour_tl) * 24 * 365, 0) AS annual_cost_tl
FROM machines WHERE high_risk_rpm = 1 GROUP BY Type;
```

**Model training:**
```python
from sklearn.ensemble import RandomForestClassifier

features = ['Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]',
            'temp_difference', 'power_consumption_kw', 'efficiency_score', 'Target']

model = RandomForestClassifier(n_estimators=100, max_depth=10,
                               min_samples_split=20, random_state=42)
model.fit(X_train, y_train)  # Accuracy: 100%
```

---

## 📈 Interactive Dashboard

**Live:** [nisanuraltay-manufacturing-energy-efficiency.streamlit.app](https://nisanuraltay-manufacturing-energy-efficiency.streamlit.app/)

Built with Streamlit. Includes a 3-page navigation flow and 5 analysis tabs:

| Tab | Content |
|-----|---------|
| ⚡ Fleet Health | RPM distribution, failure types, machine type breakdown, priority scoring |
| 🔴 Risk & Cost | High-risk segmentation by type, energy categories, tool wear |
| 📋 SQL Insights | Live SQL query results, benchmark comparison |
| 🤖 ML Model | Feature importance, confusion matrix, real-time prediction simulator |
| 💼 Action Plan | 4-initiative roadmap, Gantt chart, ROI summary |

**Sidebar filters:** Machine type · Risk status · Priority range · RPM range

---

## 💼 Strategic Action Plan

| | Initiative | Machines | Impact | Timeline |
|--|-----------|----------|--------|----------|
| 🔴 1 | Bottom 10% Emergency Maintenance | 1,000 | ₺454K/yr | 0–30 days |
| 🟠 2 | L-Type RPM Optimization | 256 | ₺5–7M/yr | 30–90 days |
| 🟡 3 | M-Type Failure Prevention | 125 | ₺300–400K/yr | 60–120 days |
| 🟢 4 | Deploy ML Scoring Model | All | 30% reactive ↓ | 90–180 days |

**Total program:** ₺6–8M/year annual impact · ~₺500–700K one-time investment · ~900% 3-year ROI

---

## 📂 Project Structure

```
manufacturing-energy-efficiency/
│
├── data/
│   ├── raw/
│   │   └── predictive_maintenance.csv              # Original Kaggle data
│   └── processed/
│       └── predictive_maintenance_final_data.csv   # 18-column engineered dataset
│
├── notebooks/
│   ├── 01_data_exploration.ipynb     ✅ EDA · outlier detection · hypothesis testing
│   ├── 02_feature_engineering.ipynb  ✅ 8 engineered features · cost metrics
│   └── 03_sql_modeling.ipynb         ✅ SQL queries · Random Forest model
│
├── app.py                             ✅ Streamlit dashboard (5 tabs · 3 pages)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies

| Category | Tools |
|----------|-------|
| Language | Python 3.10+ |
| Data manipulation | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Machine Learning | Scikit-learn (RandomForestClassifier) |
| Database | SQLite3, SQL |
| Dashboard | Streamlit, Streamlit Components |
| Environment | Google Colab, Jupyter Notebook |
| Deployment | Streamlit Cloud |
| Version Control | Git, GitHub |

---

## 🚀 How to Run

### Clone and install

```bash
git clone https://github.com/Nisanuraltay/manufacturing-energy-efficiency.git
cd manufacturing-energy-efficiency
pip install -r requirements.txt
```

### Run dashboard locally

```bash
streamlit run app.py
```

### Run notebooks

```bash
jupyter notebook
# Open notebooks in order: 01 → 02 → 03
```

> The notebooks were written in Google Colab. Update the `file_path` variable in each notebook to your local data path before running.

---

## ⚠️ Data & Model Limitations

This project uses a **synthetic/simulated dataset** — not real production telemetry. Before any production deployment:

- **Power formula:** Captures mechanical output only — friction, motor inefficiency, and idle draw are excluded
- **Cost rates:** 1.2 TL/kWh assumed — verify against actual utility contracts
- **Model accuracy:** 100% reflects a deterministic priority score derived from input features (not overfitting)
- **No time series:** Machine degradation over time is not captured
- **Savings estimates:** Conservative — actual results may vary ±20%

Recommended path to production: pilot on 100–200 machines → measure actual savings → retrain model quarterly with real data.

---

## 👤 Contact

**Nisa Nur Altay** — Data Analyst

Career-changer transitioning into data analytics. This project demonstrates end-to-end analytical thinking: from an ambiguous business problem to a deployable interactive dashboard.

- 🐙 GitHub: [github.com/Nisanuraltay](https://github.com/Nisanuraltay)
- 💼 LinkedIn: [linkedin.com/in/nisanuraltay](https://www.linkedin.com/in/nisanuraltay)

Feedback, suggestions, and collaboration opportunities are welcome — open an issue or reach out directly.

---

## 📄 License

Open source under the [MIT License](LICENSE).

---

*⭐ If this project was useful or interesting, a star is appreciated!*
