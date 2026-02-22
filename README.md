# ⚡ Manufacturing Energy Efficiency Analysis

## 👋 Project Story

This project is part of my **career transition** into data analytics. I wanted to demonstrate not just technical skills, but how I approach real business problems with data-driven thinking.

### 💡 How the Idea Was Born

I found a "predictive maintenance" dataset on Kaggle and thought:
> *"What if I reframe this as an energy efficiency problem instead?"*

I asked myself: *"If I were a consultant at a manufacturing facility, how would I approach this?"* 

That question shaped the entire analysis - from business context to ROI calculations.

### 🎢 Challenges I Faced

**Challenge 1: My first hypothesis was wrong!**

I initially thought high-risk machines were doing "light work" because:
- High RPM but low torque
- Seemed logical: Light materials = less power needed

But when I **tested this hypothesis** with the data, the failure rate was **2.6x higher!** This proved inefficiency, not light work.

**Lesson learned:** Never trust assumptions without testing them! 📊

**Challenge 2: Energy formula gave misleading results**

Simple power formula showed high-risk machines consuming "less energy." But this ignored:
- Friction losses (increases with RPM²)
- Motor inefficiency at high speeds
- Idle current draw

**Lesson learned:** Domain knowledge matters - formulas have limits! ⚠️

I pivoted to **failure cost analysis** instead - more measurable and realistic.

### 🎯 What I Accomplished

- ✅ Cleaned and analyzed 10,000 machine records
- ✅ Performed hypothesis testing (data-driven decisions)
- ✅ Applied best practices (labeled outliers instead of deleting)
- ✅ Translated technical findings into business value (227K TL/year)
- ✅ Acknowledged formula limitations honestly

---

## 🎯 Business Problem

A manufacturing facility operates 300 machines 24/7 with monthly electricity costs of ~$42,000.

**Objective:** Identify energy efficiency optimization opportunities targeting 10-15% savings.

**Potential Value:** $50,000 - $75,000 per year in savings

---

## 📊 Dataset

**Source:** [Kaggle - Machine Predictive Maintenance Classification](https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification)

- **Size:** 10,000 rows × 10 columns
- **Content:** Machine sensor data (temperature, RPM, torque, wear)
- **Reframing:** Predictive maintenance → Energy efficiency analysis

---

## 🔍 Key Findings

### 1. High-Risk Machine Detection
- **418 machines** (4.18%) exhibit abnormal operational profiles
- Average RPM: **2102** (normal: 1514) → 39% faster
- Average Torque: **18.9 Nm** (normal: 40.9) → 54% lower

### 2. Proof of Inefficiency
- High speed + low torque = **wasted energy**
- Failure rate: **8.37%** (normal: 3.17%) → **2.6x higher!**

### 3. Business Impact
- High-risk machines cost **454,826 TL/year** in failures
- **Optimization potential: ~227,000 TL/year**

### 4. Prioritization
- **L-type machines:** 256 units (61%) → Highest priority
- **M-type machines:** 125 units (30%)
- **H-type machines:** 37 units (9%)

---

## 📂 Project Structure
```
manufacturing-energy-efficiency/
│
├── data/
│   ├── raw/                          # Raw data
│   └── processed/                    # Cleaned data
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    ✅ Completed
│   ├── 02_feature_engineering.ipynb  🔄 In progress
│   ├── 03_modeling.ipynb             ⏳ Planned
│   └── 04_sql_analysis.ipynb         ⏳ Planned
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
├── images/                           # Visual materials
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 📚 My Learning Journey

### Technical Skills Developed

**Data Quality:**
- Data type validation and correction (integer → float)
- Duplicate detection
- Outlier detection using IQR method
- **Decision:** Labeled outliers instead of deleting (real-world high RPM may be valid)

**Statistical Analysis:**
- Hypothesis testing: "High-risk machines do light work" → False! (failure rate 2.6x higher)
- Correlation analysis: RPM-Torque negative correlation (-0.87)
- Comparative analysis: Normal vs High-risk

**Data-Driven Decision Making:**
- When energy formula was misleading, I pivoted to failure cost analysis
- Acknowledged domain knowledge gaps and stated assumptions clearly

### Business Skills Developed

**Value Generation:**
- Translated technical findings into financial impact (TL/year)
- Calculated cost per failure: 13,000 TL
- Identified optimization potential: 227,000 TL/year

**Executive Communication:**
- Used executive summary format
- Prioritized actions (L-type first)
- Defined clear next steps

### Problems I Solved

**1. Formula Discrepancy:**
- Simple energy formula showed high-risk as "low consumption"
- Solution: Researched physical realities (friction, efficiency)
- Decision: Used formula with warnings, focused on failure costs

**2. Hypothesis Error:**
- "Light work" hypothesis seemed logical but was wrong
- Solution: Tested with data (failure rate, wear, type distribution)
- Learned: Intuition ≠ Data!

**3. Outlier Decision:**
- Delete or keep?
- Solution: Researched best practices, chose labeling
- Rationale: High RPM may be different machine types, real-world data

### Resources Used

- **Kaggle Notebooks:** EDA techniques and visualization
- **Medium Articles:** Energy efficiency domain knowledge
- **Stack Overflow:** Pandas/Plotly troubleshooting
- **Academic Papers:** Motor energy consumption formulas
- **Mentorship:** Strategy and decision-making guidance

---

## 📓 Analysis Process

### ✅ Completed: Exploratory Data Analysis (EDA)

**What I Did:**
- Analyzed 10,000 machine records
- Data quality checks (type correction, duplicate detection)
- Outlier analysis (IQR method) - detected 418 high-risk machines
- Hypothesis testing: "Light work" hypothesis tested and rejected
- **Business value:** Calculated 227K TL/year optimization potential

**Methodology:**
- ✅ Labeled outliers instead of deleting (best practice)
- ✅ Conducted hypothesis testing (data-driven decisions)
- ✅ Interpreted formulas with domain knowledge
- ✅ Focused on business value

📓 **[Notebook: 01_data_exploration.ipynb](notebooks/01_data_exploration.ipynb)**

---

### 🔜 Planned Work

**2. Feature Engineering**
- Energy consumption metrics (kW, cost/hour)
- Efficiency scores
- Shift simulation (day/night rates)

**3. SQL Analysis**
- Cost segmentation (type/shift-based)
- Bottom 10% machines by efficiency
- Optimization prioritization

**4. Predictive Model**
- "Which machine to optimize?" prediction
- Feature importance analysis
- Risk scoring

**5. Power BI Dashboard**
- Executive summary
- Machine performance tracking
- Interactive optimization recommendations

---

## 🛠️ Technologies Used

**Analysis & Modeling:**
- Python 3.x
- Pandas, NumPy (data manipulation)
- Matplotlib, Seaborn, Plotly (visualization)
- Scikit-learn (machine learning)

**Database:**
- SQLite (local analysis)
- SQL (cost segmentation)

**Reporting:**
- Power BI (interactive dashboard)
- Jupyter Notebook (technical documentation)

**Version Control:**
- Git & GitHub

---

## 🚀 How to Run

### 1. Clone Repository
```bash
git clone https://github.com/Nisanuraltay/manufacturing-energy-efficiency.git
cd manufacturing-energy-efficiency
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run Notebooks
```bash
jupyter notebook
```

**Note:** Download dataset from [Kaggle](https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification) to `data/raw/`

---

## 📌 Project Goals

This project was developed during my **career transition** to demonstrate data analytics capabilities.

**Focus areas:**
- ✅ Solving real business problems
- ✅ Data-driven decision making
- ✅ Business value calculation (TL/year)
- ✅ Professional reporting
- ✅ End-to-end project management

---

## 📊 Next Steps

1. ⏳ Feature engineering and energy metrics
2. ⏳ Deep-dive SQL cost analysis
3. ⏳ Machine learning model (optimization prioritization)
4. ⏳ Power BI dashboard development
5. ⏳ Executive report preparation

---

## 👤 Contact

**Project Owner:** Nisa Nur Altay

I'm a career changer transitioning into data analytics. This project is part of my portfolio, demonstrating how I approach real business problems.

**GitHub:** [github.com/Nisanuraltay](https://github.com/Nisanuraltay)

**LinkedIn:** [www.linkedin.com/in/nisanuraltay] 

📧 **Feel free to reach out for feedback or opportunities.**

---

## 💭 Feedback & Improvements

I'm continuously improving this project. If you:
- Notice a technical error
- Have a different analytical approach to suggest
- Want to collaborate

**Open an issue or contact me directly!**

Constructive criticism is welcome - I'm here to learn! 🚀

---

## 📄 License

This project is open source under the MIT License.

---

**⭐ If you found this project helpful, please consider giving it a star!**
