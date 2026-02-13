# 🔁 ReGenesis – Circular Economy Intelligence Engine

<p align="center">
  <img src="https://user-images.githubusercontent.com/your-username/regenesis-banner.png" alt="ReGenesis Banner" width="800">
</p>

**ReGenesis** is an interactive, data-driven Streamlit application that helps entrepreneurs evaluate waste recycling opportunities, simulate environmental impact, generate strategic roadmaps, and produce actionable business blueprints — all grounded in real data.

---
## ELITE STRATOS 
# member 1: Sreelakshmi P V 
# member 2: Muhsina S M 

## 📦 Table of Contents

| Section | Description |
|---------|-------------|
| 🎯 Overview | What is ReGenesis? |
| 🚀 Features | Platform capabilities |
| 📊 Screens | UI walkthrough |
| 🧠 How It Works | Scoring + logic |
| 🛠 Tech Stack | Technologies used |
| 📥 Installation | Setup instructions |
| ▶️ Usage | Run & demo |
| 📁 File Structure | Project layout |
| 🙌 Contributors | Credits |
| 📄 License | Open source info |

---
##  Technologies Used

### Frontend & UI
- Streamlit – Interactive web application framework
- Custom CSS (Glassmorphism Design) – Premium UI styling
- HTML inside Streamlit – Advanced layout customization

###  Data Processing
- Pandas – Data manipulation & preprocessing
- OpenPyXL – Excel file handling
- CSV & Excel Datasets – Market & waste analysis

### Business Intelligence Logic
- Feasibility Scoring Algorithm
- Scale Multiplier Model
- Environmental Pressure Normalization
- Weekly Roadmap Generator Logic

###  Export & Reporting
- ReportLab – Dynamic PDF roadmap generation

###  Backend
- Python 3.x
- Streamlit state management
- Caching using @st.cache_data


##  Overview

ReGenesis enables waste-to-value innovation with:

- Feasibility analysis of recycling opportunities
- Impact simulation including CO₂ and job metrics
- Dynamic action plan generation
- Strategic startup blueprint generation
- Clean, responsive, premium UI

Perfect for hackathons, circular economy builders, and environmental entrepreneurs.

---

##  Features

###  Layer 1 – Opportunity Dashboard
- Revenue estimation
- Mismanaged waste analysis
- Scale & feasibility scoring
- Animated progress indicator

###  Layer 2 – Impact Simulator
- 6-month revenue
- CO₂ reduced
- Jobs created
- Plastic diverted

### Layer 3 – Weekly Roadmap Generator
- Dynamic 1–24 week roadmap
- Visual timeline
- Downloadable PDF

###  Layer 4 – Strategic Blueprint Generator
- Smart startup strategy recommendations
- KPI summary cards
- Risk, scaling plan, revenue model

---

##  Screens
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/38555edc-658c-4e65-b717-4052fce74805" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/002a777a-70d3-4524-b32c-4fd8863acf19" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ab70b026-c28d-4dee-a293-9decbf46f161" />

## video



https://github.com/user-attachments/assets/f78f49f2-25c3-4cae-8e07-3ae7334f5a34


## 🧠 How It Works

### ✔ Feasibility Score

The feasibility score is calculated using:

- **Market price**
- **Demand score**
- **Scale multiplier**
- **Environmental pressure factor**


Where:
- `scale_factor = 1 + (quantity / 500)`

High scores indicate strong business opportunity.

---
# TRY THE LIVE APP ON STREAMLIT
https://regenesis-aszqp9rzk9usv7kxjsyaez.streamlit.app/

##  Tech Stack

| Category | Tools |
|----------|-------|
| UI | Streamlit |
| Data | pandas, Excel/CSV |
| PDF Export | ReportLab |
| Visual Styles | Custom CSS |
| Interactive Elements | Streamlit widgets |

---

## 📥 Installation

### 1. Clone the repo
```bash
git clone https://github.com/SREELAKSHMI-PV-07/regenesis/blob/650810cba3ac20f465530ec737860c8b4686b6f3/app.py
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
streamlit run app.py

ReGenesis/
│── app.py
│── plastic_market_prices.csv
│── country_data.xlsx
│── requirements.txt
│── README.md
| Name           | Role                   |
| -------------- | ---------------------- |
| Sreelakshmi PV | Co-Founder / Developer |
| Muhsina S M    | Co-Founder / Developer |
License

This project is MIT Licensed — feel free to use or extend.

 Support / Feedback

If you found ReGenesis useful, give it a ⭐on GitHub!

<p align="center"> <b>Built with ♻️ by Sreelakshmi PV &amp; Muhsina S M</b> </p> ```
