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

/* Global Background */
.stApp {
    background: linear-gradient(135deg,#0B1120,#020617);
    color: white;
    font-family: 'Inter', sans-serif;
}

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

/* Section Title (used for Impact + Action Plan) */
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

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#2ECC71,#16A085);
    color: white;
    border-radius: 30px;
    border: none;
    padding: 10px 25px;
    font-weight: 600;
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
    country_df = country_df.dropna(subset=["country"]).reset_index(drop=True)

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
    country = st.selectbox("Select Country", sorted(country_df["country"].unique()))

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

# ---------------- DASHBOARD ----------------
st.markdown("## 📊 Opportunity Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Revenue Potential (₹)</div><div class='card-value'>{round(market_value,2):,}</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Mismanaged Waste (MT)</div><div class='card-value'>{mismanaged:,.0f}</div></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Scale Multiplier</div><div class='card-value'>{round(scale_factor,2)}</div></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='glass-card'><div class='card-title'>Feasibility Score</div><div class='card-value'>{feasibility_score}</div></div>", unsafe_allow_html=True)

# -------- Sliding Progress Bar --------
st.markdown("<br>", unsafe_allow_html=True)

progress = st.progress(0)
for i in range(int(feasibility_score)):
    time.sleep(0.005)
    progress.progress(i + 1)

st.markdown(
    f"<div style='text-align:center; margin-top:8px; color:#2ECC71; font-weight:600;'>"
    f"{feasibility_score} / 100"
    "</div>",
    unsafe_allow_html=True
)

# ---------------- IMPACT SIMULATOR ----------------
st.markdown("<div class='section-title'>Impact Simulator</div>", unsafe_allow_html=True)

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

# ---------------- ACTION PLAN ----------------
# ---------------- ACTION PLAN ----------------
st.markdown("<div class='section-title'>Startup Action Plan</div>", unsafe_allow_html=True)

weeks = st.slider("Select Roadmap Duration (Weeks)", 1, 24, 8)

if st.button("🚀 Generate Action Plan"):

    st.success("Your personalized roadmap is ready!")

    roadmap_text = f"""
STARTUP ROADMAP

Waste Type: {waste_type}
Country: {country.title()}
Feasibility Score: {feasibility_score}

-----------------------------------------
"""

    # Weekly roadmap generation
    for week in range(1, weeks + 1):

        if week <= 4:
            task = "Market research, supplier identification, waste sourcing validation."
            color = "#22C55E"

        elif week <= 8:
            task = "Prototype development, recycling process testing, cost optimization."
            color = "#EAB308"

        elif week <= 12:
            task = "Pilot production, early customers onboarding, revenue tracking."
            color = "#F97316"

        elif week <= 16:
            task = "Operational improvements, branding, compliance approvals."
            color = "#3B82F6"

        else:
            task = "Scaling operations, partnerships, marketing expansion, investor outreach."
            color = "#EF4444"

        # Display in UI
        st.markdown(f"""
        <div class='timeline-card' style='border-color:{color};'>
            <div class='phase-title'>Week {week}</div>
            <div class='phase-content'>{task}</div>
        </div>
        """, unsafe_allow_html=True)

        # Add to PDF text
        roadmap_text += f"\nWeek {week}: {task}\n"

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
    #layer 4
import google.generativeai as genai
import os

# ---------------- LAYER 4 ----------------
st.divider()

st.markdown("<div class='section-title'>AI Startup Blueprint</div>", unsafe_allow_html=True)

st.markdown("""
Turn your feasibility analysis into a complete startup blueprint using AI.
""")

# -------- Gemini Setup --------
import google.generativeai as genai

try:
    genai.configure(api_key=st.secrets["AIzaSyB_CH5d-b01ixW22pj8VRPziTG--n8QAlg"])
except Exception:
    st.error("Google API Key not found. Please add it in Streamlit Secrets.")
    st.stop()

if st.button("🚀 Generate AI Startup Blueprint"):

    with st.spinner("Building your circular startup..."):

        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")

            prompt = f"""
You are a professional circular economy startup mentor.

Context:
Waste Type: {waste_type}
Country: {country}
Feasibility Score: {feasibility_score}

Generate a structured startup blueprint with clear headings:

1. Startup Name
2. Problem Statement
3. Solution
4. Revenue Model
5. 6 Month Action Plan
6. 30 Second Investor Pitch

Make it realistic, practical, and aligned with feasibility score.
Keep formatting clean with headings.
"""

            response = model.generate_content(prompt)

            ai_text = response.text

            st.success("Your AI Startup Blueprint is ready!")

            # -------- Premium Card Styling --------
            st.markdown("""
            <style>
            .generator-card {
                background: rgba(255,255,255,0.05);
                padding:30px;
                border-radius:20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                margin-top:20px;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="generator-card">', unsafe_allow_html=True)
            st.markdown(ai_text)
            st.markdown('</div>', unsafe_allow_html=True)

            # -------- PDF Download --------
            styles = getSampleStyleSheet()
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            doc = SimpleDocTemplate(tmp_file.name)
            story = []

            for line in ai_text.split("\n"):
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 6))

            doc.build(story)

            with open(tmp_file.name, "rb") as f:
                st.download_button(
                    label="📄 Download AI Blueprint PDF",
                    data=f,
                    file_name="ai_startup_blueprint.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error("AI generation failed. Please check model access or billing in Google Cloud.")
