import streamlit as st
import pandas as pd
import math
import time
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ReGenesis",
    page_icon="♻️",
    layout="wide"
)

# ---------------- PREMIUM DESIGN ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0B1120,#020617);
    color: white;
    font-family: 'Inter', sans-serif;
}

hr { border: none; }

.hero {
    text-align:center;
    padding-top:50px;
    padding-bottom:40px;
}

.hero h1 {
    font-size:60px;
    font-weight:700;
    background: linear-gradient(90deg,#2ECC71,#16A085);
    -webkit-background-clip:text;
    color:transparent;
}

.hero p {
    font-size:20px;
    color:#94A3B8;
}

.section-title {
    text-align: center;
    font-size: 36px;
    font-weight: 600;
    margin-top: 90px;
    margin-bottom: 40px;
    background: linear-gradient(90deg,#2ECC71,#16A085);
    -webkit-background-clip: text;
    color: transparent;
}

.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    transition: 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-6px);
}

.card-title {
    font-size: 15px;
    color: #94A3B8;
}

.card-value {
    font-size: 32px;
    font-weight: 700;
    margin-top: 10px;
    color: #2ECC71;
}

.timeline-card {
    background: rgba(255,255,255,0.04);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    border-left: 6px solid;
    backdrop-filter: blur(8px);
    transition: 0.3s ease;
}

.timeline-card:hover {
    transform: translateX(6px);
}

.phase-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}

.phase-content {
    font-size: 14px;
    color: #CBD5E1;
}

.stButton>button {
    background: linear-gradient(90deg,#2ECC71,#16A085);
    color: white;
    border-radius: 30px;
    border: none;
    padding: 10px 25px;
    font-weight: 600;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg,#2ECC71,#16A085);
}

/* FOOTER */
.footer {
    margin-top: 120px;
    padding: 50px 20px;
    width: 100%;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255,255,255,0.08);
    text-align: center;
}

.footer-container {
    max-width: 1200px;
    margin: auto;
}

.footer-title {
    font-size: 18px;
    font-weight: 600;
    background: linear-gradient(90deg,#2ECC71,#16A085);
    -webkit-background-clip:text;
    color:transparent;
    margin-bottom: 10px;
}

.footer-sub {
    font-size: 14px;
    color: #94A3B8;
    margin-bottom: 15px;
}

.footer-icons {
    font-size: 20px;
    margin-bottom: 15px;
}

.footer-bottom {
    font-size: 12px;
    color: #64748B;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    market_df = pd.read_csv("plastic_market_prices.csv")
    market_df.columns = market_df.columns.str.strip()
    country_df = pd.read_excel("country_data.xlsx")
    country_df = country_df.iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]
    country_df["country"] = country_df["country"].astype(str).str.strip().str.lower()
    country_df["mismanaged"] = pd.to_numeric(country_df["mismanaged"], errors="coerce")
    return market_df, country_df

market_df, country_df = load_data()

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>ReGenesis</h1>
    <p>Circular Economy Intelligence Engine</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
col1, col2, col3 = st.columns(3)

with col1:
    waste_type = st.selectbox("Select Waste Type", market_df["category"].unique())

with col2:
    quantity = st.number_input("Enter Quantity (kg)", min_value=1, step=10, value=100)

with col3:
    country = st.selectbox("Select Country", sorted(country_df["country"].unique()))

# ---------------- CALCULATIONS ----------------
row = market_df[market_df["category"] == waste_type].iloc[0]
price_usd = float(row["avg_price_per_kg_usd"])
demand_score = float(row["demand_score_1_to_10"])

mismanaged = country_df.loc[country_df["country"] == country, "mismanaged"].values
mismanaged = float(mismanaged[0]) if len(mismanaged) else 0

price_inr = price_usd * 80
market_value = quantity * price_inr
scale_factor = 1 + (quantity / 500)

raw_score = (price_usd * demand_score) * scale_factor
feasibility_score = round(min(100, raw_score), 2)

# ---------------- DASHBOARD ----------------
st.markdown("## 📊 Opportunity Dashboard")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Revenue Potential (₹)</div><div class='card-value'>{round(market_value,2):,}</div></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Mismanaged Waste (MT)</div><div class='card-value'>{mismanaged:,.0f}</div></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Scale Multiplier</div><div class='card-value'>{round(scale_factor,2)}</div></div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Feasibility Score</div><div class='card-value'>{feasibility_score}</div></div>", unsafe_allow_html=True)

progress = st.progress(0)
for i in range(int(feasibility_score)):
    time.sleep(0.003)
    progress.progress(i+1)

st.markdown(f"<div style='text-align:center;color:#2ECC71;font-weight:600;'>{feasibility_score} / 100</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <div class="footer-container">
        <div class="footer-title">ReGenesis</div>
        <div class="footer-sub">Circular Economy Intelligence Platform</div>
        <div class="footer-icons">🌍 ♻️ 📊 🚀</div>
        <div class="footer-bottom">
            Built by <b>Sreelakshmi PV</b> & <b>Muhsina S M</b><br><br>
            © 2026 ReGenesis | Built for Sustainable Innovation
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
