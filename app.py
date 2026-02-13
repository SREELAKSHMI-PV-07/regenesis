import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="ReGenesis – Layer 1",
    page_icon="♻️",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    market_df = pd.read_csv("plastic_market_prices.csv")

    country_df = pd.read_excel("country_data.xlsx")
    country_df = country_df.iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]

    # Clean
    country_df["country"] = (
        country_df["country"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    country_df["mismanaged"] = pd.to_numeric(
        country_df["mismanaged"], errors="coerce"
    )

    # Remove rows where mismanaged is NaN
    country_df = country_df.dropna(subset=["mismanaged"])

    return market_df, country_df


market_df, country_df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("♻️ ReGenesis – Feasibility Intelligence Engine")
st.markdown("### Layer 1: Opportunity & Feasibility Analysis")
st.divider()

# -----------------------------
# Inputs
# -----------------------------
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
        step=1
    )

with col3:
    country = st.selectbox(
        "Select Country",
        sorted(country_df["country"].unique())
    )

st.divider()

# -----------------------------
# Market Data
# -----------------------------
market_row = market_df[market_df["category"] == waste_type].iloc[0]

price_usd = float(market_row["avg_price_per_kg_usd"])
demand_score = float(market_row["demand_score_1_to_10"])

# -----------------------------
# Country Data
# -----------------------------
country_row = country_df[country_df["country"] == country].iloc[0]

mismanaged = float(country_row["mismanaged"])

# -----------------------------
# Calculations
# -----------------------------
price_inr = price_usd * 80
market_value = quantity * price_inr

# Environmental pressure scaling
env_factor = mismanaged / country_df["mismanaged"].max()

# Production scale factor
scale_factor = quantity / 100

# Core feasibility formula
raw_score = price_usd * demand_score * env_factor * scale_factor

feasibility_score = round(min(100, raw_score * 8), 2)

# -----------------------------
# Status
# -----------------------------
if feasibility_score < 30:
    status = "🔴 High Risk"
elif feasibility_score < 70:
    status = "🟡 Moderate Opportunity"
else:
    status = "🟢 High Potential"

# -----------------------------
# Dashboard
# -----------------------------
st.subheader("📊 Opportunity Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("💰 Market Value (₹)", f"{round(market_value,2):,}")
c2.metric("🌍 Mismanaged Index", round(mismanaged,2))
c3.metric("📈 Feasibility Score", feasibility_score)

st.markdown(f"### Status: {status}")

st.divider()

with st.expander("ℹ️ How Feasibility Score Works"):
    st.write("""
• Market price & demand  
• Environmental pressure (mismanaged waste)  
• Production scale  

The score dynamically adjusts based on selected country, waste type, and scale.
""")

st.caption("ReGenesis – Circular Economy Intelligence | Layer 1 MVP")
