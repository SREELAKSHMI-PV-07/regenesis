import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ReGenesis – Layer 1",
    page_icon="♻️",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():

    # -------- MARKET DATA --------
    market_df = pd.read_csv("plastic_market_prices.csv")
    market_df.columns = market_df.columns.str.strip()
    market_df = market_df.loc[:, ~market_df.columns.str.contains("^Unnamed")]

    # -------- COUNTRY DATA --------
    country_df = pd.read_excel("country_data.xlsx")
    country_df = country_df.dropna(axis=1, how="all")
    country_df = country_df.iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]

    country_df["country"] = (
        country_df["country"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    country_df["mismanaged"] = pd.to_numeric(
        country_df["mismanaged"],
        errors="coerce"
    )

    country_df = country_df.dropna(subset=["country"])
    country_df = country_df.reset_index(drop=True)

    return market_df, country_df


market_df, country_df = load_data()

# ---------------- TITLE ----------------
st.title("♻️ ReGenesis – Feasibility Intelligence Engine")
st.markdown("### Layer 1: Opportunity & Feasibility Analysis")
st.divider()

# ---------------- USER INPUT ----------------
col1, col2, col3 = st.columns(3)

with col1:
    waste_type = st.selectbox(
        "Select Waste Type",
        market_df["category"].unique()
    )

with col2:
    quantity = st.number_input(
        "Enter Quantity (kg)",
        min_value=1,
        step=10,
        value=100
    )

with col3:
    country_list = sorted(country_df["country"].unique())

    if len(country_list) == 0:
        st.error("No country data found. Please check country_data.xlsx")
        st.stop()

    country = st.selectbox("Select Country", country_list)

selected_country = str(country).lower().strip()

st.divider()

# ---------------- MARKET DATA ----------------
row = market_df[market_df["category"] == waste_type].iloc[0]

price_usd = float(row["avg_price_per_kg_usd"])
demand_score = float(row["demand_score_1_to_10"])

# ---------------- COUNTRY MATCH ----------------
match = country_df[country_df["country"] == selected_country]

if match.empty:
    mismanaged = 0
else:
    mismanaged = float(match["mismanaged"].values[0])

# ---------------- NORMALIZE METRIC TONNES ----------------
# Normalize relative to max country waste to avoid score explosion
max_mismanaged = country_df["mismanaged"].max()

if max_mismanaged > 0:
    mismanaged_normalized = mismanaged / max_mismanaged
else:
    mismanaged_normalized = 0

# ---------------- INTEGRATED MODEL ----------------

price_inr = price_usd * 80
market_value = quantity * price_inr

scale_factor = 1 + (quantity / 500)

# Use normalized tonnage in scoring
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
st.subheader("📊 Opportunity Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Revenue Potential (₹)", f"{round(market_value,2):,}")

# ✅ Added (Metric Tonnes) label + formatted number
c2.metric("🌍 Mismanaged Waste (Metric Tonnes)", f"{mismanaged:,.0f}")

c3.metric("📦 Scale Multiplier", round(scale_factor, 2))
c4.metric("📈 Feasibility Score", feasibility_score)

st.markdown(f"### Status: {status}")

# ---------------- FEASIBILITY EXPLANATION ----------------
st.markdown("### 🎯 What the Feasibility Score Means")

if feasibility_score < 30:
    st.error("0–30: Low Opportunity. High risk and limited profitability potential.")
elif feasibility_score < 70:
    st.warning("30–70: Moderate Opportunity. Needs optimization and strategic planning.")
else:
    st.success("70–100: High Potential. Strong market, scale, and environmental advantage.")

st.divider()

# ---------------- INFO SECTION ----------------
with st.expander("ℹ️ How Feasibility Score Works"):
    st.write("""
• Market strength → Price × Demand  
• Scale efficiency → Larger quantities improve viability  
• Environmental pressure → Higher mismanaged waste increases opportunity  

Mismanaged waste is represented in Metric Tonnes and normalized relative to the highest observed country value.
""")

st.caption("ReGenesis – Circular Economy Intelligence | Layer 1 MVP")



import math
import time

st.subheader("🌱 Layer 2 – Impact Simulator")

# -------------------------------------------------
# ICON ROW (Images)
# -------------------------------------------------
img1, img2, img3, img4 = st.columns(4)

img1.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=60)
img2.image("https://cdn-icons-png.flaticon.com/512/2933/2933894.png", width=60)
img3.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=60)
img4.image("https://cdn-icons-png.flaticon.com/512/427/427735.png", width=60)

# -------------------------------------------------
# CALCULATIONS
# -------------------------------------------------

# Revenue projection (6 months)
monthly_revenue = market_value * 22
six_month_revenue = monthly_revenue * 6

# CO2 reduction (approx 2.5kg per kg plastic)
co2_saved = quantity * 2.5

# Job creation (1 job per 500kg/month)
jobs_created = max(1, math.ceil((quantity * 22) / 500))

# Plastic diverted (based on mismanaged %)
plastic_diverted = quantity * (mismanaged / 100)

# -------------------------------------------------
# METRICS
# -------------------------------------------------

i1, i2, i3, i4 = st.columns(4)

i1.metric("📆 6-Month Revenue (₹)", f"{round(six_month_revenue,2):,}")
i2.metric("🌍 CO₂ Reduced (kg)", round(co2_saved,2))
i3.metric("👷 Jobs Created", jobs_created)
i4.metric("🌊 Plastic Diverted (kg)", round(plastic_diverted,2))

st.divider()

# -------------------------------------------------
# 🔥 Animated Feasibility Progress Bar
# -------------------------------------------------

st.markdown("### ⚡ Feasibility Progress")

progress = st.progress(0)

for i in range(int(feasibility_score)):
    time.sleep(0.01)
    progress.progress(i + 1)

st.caption(f"Current Feasibility: {feasibility_score}%")

st.divider()

# -------------------------------------------------
# 🎛 Scenario Buttons (Mini Layer 3)
# -------------------------------------------------

st.subheader("🎛 Growth Scenario")

scenario = st.radio(
    "Choose scenario:",
    ["Conservative", "Balanced", "Aggressive"],
    horizontal=True
)

if scenario == "Conservative":
    multiplier = 0.7
elif scenario == "Balanced":
    multiplier = 1.0
else:
    multiplier = 1.4

scenario_revenue = six_month_revenue * multiplier

st.metric("📊 Scenario 6-Month Revenue (₹)", f"{round(scenario_revenue,2):,}")

# -------------------------------------------------
# Explanation
# -------------------------------------------------

with st.expander("ℹ️ How Impact is Calculated"):
    st.write("""
📆 Revenue → Daily value × 22 days × 6 months  

🌍 CO₂ → ~2.5kg saved per kg recycled  

👷 Jobs → 1 job per 500kg/month  

🌊 Plastic diverted → Quantity × Mismanaged %

These are conservative MVP estimates for hackathon demonstration.
""")

#action plan 
import io
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.subheader("🗺️ Layer 3 – Action Plan Generator")

# -------- Week Selector --------
weeks = st.slider("Select Roadmap Duration (Weeks)", 4, 24, 12)

# -------- Phase Icons --------
p1, p2, p3, p4, p5 = st.columns(5)

p1.image("https://cdn-icons-png.flaticon.com/512/1828/1828817.png", width=50)
p2.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=50)
p3.image("https://cdn-icons-png.flaticon.com/512/190/190411.png", width=50)
p4.image("https://cdn-icons-png.flaticon.com/512/4320/4320372.png", width=50)
p5.image("https://cdn-icons-png.flaticon.com/512/1828/1828970.png", width=50)

# -------- Generate Plan --------
if st.button("🚀 Generate Action Plan"):

    roadmap_text = f"""
STARTUP ROADMAP
Waste Type: {waste_type}
Country: {country.title()}
Feasibility Score: {feasibility_score}%

"""

    st.success("Your personalized roadmap is ready!")

    # Phase 1 (Weeks 1–4)
    if weeks >= 4:
        phase1 = """
PHASE 1 – DISCOVERY (Weeks 1–4)
• Validate waste sourcing
• Visit recyclers
• Market research
• Customer interviews
"""
        st.markdown("### 🟢 Phase 1 – Discovery (Weeks 1–4)")
        st.write(phase1)
        roadmap_text += phase1

    # Phase 2 (Weeks 5–8)
    if weeks >= 8:
        phase2 = """
PHASE 2 – PROTOTYPE (Weeks 5–8)
• Build MVP
• Test recycling flow
• CO₂ estimation
• Prepare pitch deck
"""
        st.markdown("### 🟡 Phase 2 – Prototype (Weeks 5–8)")
        st.write(phase2)
        roadmap_text += phase2

    # Phase 3 (Weeks 9–12)
    if weeks >= 12:
        phase3 = """
PHASE 3 – PILOT (Weeks 9–12)
• Pilot batches
• Revenue tracking
• Operational optimization
• First customers
"""
        st.markdown("### 🟠 Phase 3 – Pilot (Weeks 9–12)")
        st.write(phase3)
        roadmap_text += phase3

    # Phase 4 (Weeks 13–16)
    if weeks >= 16:
        phase4 = """
PHASE 4 – OPTIMIZATION (Weeks 13–16)
• Improve efficiency
• Strengthen partnerships
• Apply for grants
• Impact reporting
"""
        st.markdown("### 🔵 Phase 4 – Optimization (Weeks 13–16)")
        st.write(phase4)
        roadmap_text += phase4

    # Phase 5 (Weeks 17+)
    if weeks >= 20:
        phase5 = f"""
PHASE 5 – SCALE (Weeks 17–{weeks})
• Expand sourcing
• Finalize pricing
• Marketing launch
• Investor/demo prep
"""
        st.markdown(f"### 🔴 Phase 5 – Scale (Weeks 17–{weeks})")
        st.write(phase5)
        roadmap_text += phase5

    # -------- PDF Download --------
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
