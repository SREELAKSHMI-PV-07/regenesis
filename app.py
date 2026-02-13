import streamlit as st
import pandas as pd
import math
import time
import io
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ReGenesis – Layer 1",
    page_icon="♻️",
    layout="wide"
)

# ---------------- PREMIUM DESIGN ----------------
st.markdown("""
<style>

/* Global Background */
.stApp {
    background: linear-gradient(135deg,#0B1120,#020617);
    color: white;
    font-family: 'Inter', sans-serif;
}

/* Remove Default Divider */
hr { border: none; }

/* Hero */
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

/* Glass Cards */
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

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#2ECC71,#16A085);
    color: white;
    border-radius: 30px;
    border: none;
    padding: 10px 25px;
    font-weight: 600;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* Progress Bar */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg,#2ECC71,#16A085);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    market_df = pd.read_csv("plastic_market_prices.csv")
    market_df.columns = market_df.columns.str.strip()
    market_df = market_df.loc[:, ~market_df.columns.str.contains("^Unnamed")]

    country_df = pd.read_excel("country_data.xlsx")
    country_df = country_df.dropna(axis=1, how="all")
    country_df = country_df.iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]

    country_df["country"] = country_df["country"].astype(str).str.strip().str.lower()
    country_df["mismanaged"] = pd.to_numeric(country_df["mismanaged"], errors="coerce")

    country_df = country_df.dropna(subset=["country"])
    country_df = country_df.reset_index(drop=True)

    return market_df, country_df


market_df, country_df = load_data()

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>ReGenesis</h1>
    <p>Circular Economy Intelligence Engine</p>
</div>
""", unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
col1, col2, col3 = st.columns(3)

with col1:
    waste_type = st.selectbox("Select Waste Type", market_df["category"].unique())

with col2:
    quantity = st.number_input("Enter Quantity (kg)", min_value=1, step=10, value=100)

with col3:
    country_list = sorted(country_df["country"].unique())
    country = st.selectbox("Select Country", country_list)

selected_country = str(country).lower().strip()

# ---------------- CALCULATIONS ----------------
row = market_df[market_df["category"] == waste_type].iloc[0]
price_usd = float(row["avg_price_per_kg_usd"])
demand_score = float(row["demand_score_1_to_10"])

match = country_df[country_df["country"] == selected_country]
mismanaged = float(match["mismanaged"].values[0]) if not match.empty else 0

max_mismanaged = country_df["mismanaged"].max()
mismanaged_normalized = mismanaged / max_mismanaged if max_mismanaged > 0 else 0

price_inr = price_usd * 80
market_value = quantity * price_inr
scale_factor = 1 + (quantity / 500)
mismanaged_factor = 1 + (mismanaged_normalized * 3)

raw_score = (price_usd * demand_score) * scale_factor * mismanaged_factor
feasibility_score = round(min(100, raw_score), 2)

# ---------------- STATUS ----------------
if feasibility_score < 30:
    status = "🔴 High Risk"
elif feasibility_score < 70:
    status = "🟡 Moderate Opportunity"
else:
    status = "🟢 High Potential"

# ---------------- DASHBOARD ----------------
st.markdown("## 📊 Opportunity Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title">Revenue Potential (₹)</div>
        <div class="card-value">{round(market_value,2):,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title">Mismanaged Waste (MT)</div>
        <div class="card-value">{mismanaged:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title">Scale Multiplier</div>
        <div class="card-value">{round(scale_factor,2)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title">Feasibility Score</div>
        <div class="card-value">{feasibility_score}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"### Status: {status}")

# ---------------- PROGRESS ----------------
st.markdown("### ⚡ Feasibility Progress")
progress = st.progress(0)
for i in range(int(feasibility_score)):
    time.sleep(0.01)
    progress.progress(i + 1)

st.caption(f"Current Feasibility: {feasibility_score}%")

# ---------------- LAYER 2 ----------------
st.markdown("## 🌱 Layer 2 – Impact Simulator")

monthly_revenue = market_value * 22
six_month_revenue = monthly_revenue * 6
co2_saved = quantity * 2.5
jobs_created = max(1, math.ceil((quantity * 22) / 500))
plastic_diverted = quantity * (mismanaged / 100)

i1, i2, i3, i4 = st.columns(4)

i1.metric("📆 6-Month Revenue (₹)", f"{round(six_month_revenue,2):,}")
i2.metric("🌍 CO₂ Reduced (kg)", round(co2_saved,2))
i3.metric("👷 Jobs Created", jobs_created)
i4.metric("🌊 Plastic Diverted (kg)", round(plastic_diverted,2))

# ---------------- LAYER 3 ----------------
# ---------------- LAYER 3 ----------------
# ---------------- LAYER 3 ----------------
# ---------------- LAYER 3 ----------------
st.markdown("## 🗺️ Layer 3 – Action Plan Generator")

# -------- Timeline Styling --------
st.markdown("""
<style>

/* Timeline Card */
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

</style>
""", unsafe_allow_html=True)

weeks = st.slider("Select Roadmap Duration (Weeks)", 4, 24, 12)

if st.button("🚀 Generate Action Plan"):

    st.success("Your personalized roadmap is ready!")

    roadmap_text = f"""
STARTUP ROADMAP

Waste Type: {waste_type}
Country: {country.title()}
Feasibility Score: {feasibility_score}%

-----------------------------------------
"""

    # -------- PHASE 1 --------
    if weeks >= 1:
        phase1 = """
• Validate waste sourcing  
• Visit recyclers  
• Conduct market research  
• Identify first customers
"""
        st.markdown(f"""
        <div class="timeline-card" style="border-color:#22C55E;">
            <div class="phase-title">🟢 Phase 1 – Discovery (Weeks 1–4)</div>
            <div class="phase-content">{phase1}</div>
        </div>
        """, unsafe_allow_html=True)

        roadmap_text += "\nPHASE 1 – DISCOVERY (Weeks 1–4)\n" + phase1

    # -------- PHASE 2 --------
    if weeks >= 5:
        phase2_end = min(weeks, 8)

        phase2 = """
• Build minimum viable product  
• Test recycling workflow  
• Calculate CO₂ savings  
• Prepare pitch deck
"""
        st.markdown(f"""
        <div class="timeline-card" style="border-color:#EAB308;">
            <div class="phase-title">🟡 Phase 2 – Prototype (Weeks 5–{phase2_end})</div>
            <div class="phase-content">{phase2}</div>
        </div>
        """, unsafe_allow_html=True)

        roadmap_text += f"\nPHASE 2 – PROTOTYPE (Weeks 5–{phase2_end})\n" + phase2

    # -------- PHASE 3 --------
    if weeks >= 9:
        phase3_end = min(weeks, 12)

        phase3 = """
• Run pilot batches  
• Track revenue  
• Optimize operations  
• Secure early adopters
"""
        st.markdown(f"""
        <div class="timeline-card" style="border-color:#F97316;">
            <div class="phase-title">🟠 Phase 3 – Pilot (Weeks 9–{phase3_end})</div>
            <div class="phase-content">{phase3}</div>
        </div>
        """, unsafe_allow_html=True)

        roadmap_text += f"\nPHASE 3 – PILOT (Weeks 9–{phase3_end})\n" + phase3

    # -------- PHASE 4 --------
    if weeks >= 13:
        phase4_end = min(weeks, 16)

        phase4 = """
• Improve efficiency  
• Strengthen supplier partnerships  
• Apply for green grants  
• Develop branding strategy
"""
        st.markdown(f"""
        <div class="timeline-card" style="border-color:#3B82F6;">
            <div class="phase-title">🔵 Phase 4 – Optimization (Weeks 13–{phase4_end})</div>
            <div class="phase-content">{phase4}</div>
        </div>
        """, unsafe_allow_html=True)

        roadmap_text += f"\nPHASE 4 – OPTIMIZATION (Weeks 13–{phase4_end})\n" + phase4

    # -------- PHASE 5 --------
    if weeks >= 17:
        phase5 = """
• Expand sourcing network  
• Launch marketing campaigns  
• Approach investors  
• Scale production
"""
        st.markdown(f"""
        <div class="timeline-card" style="border-color:#EF4444;">
            <div class="phase-title">🔴 Phase 5 – Scale (Weeks 17–{weeks})</div>
            <div class="phase-content">{phase5}</div>
        </div>
        """, unsafe_allow_html=True)

        roadmap_text += f"\nPHASE 5 – SCALE (Weeks 17–{weeks})\n" + phase5

    # -------- PDF GENERATION --------
    styles = getSampleStyleSheet()
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp_file.name, pagesize=A4)
    story = []

    for line in roadmap_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 6))

    doc.build(story)

    with open(tmp_file.name, "rb") as f:
        st.download_button(
            label="📄 Download Roadmap PDF",
            data=f,
            file_name="regenesis_action_plan.pdf",
            mime="application/pdf"
        )
