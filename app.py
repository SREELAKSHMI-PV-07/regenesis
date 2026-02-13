import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
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
    country_df = pd.read_excel("country_data.xlsx").iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]
    return market_df, country_df

market_df, country_df = load_data()

# -----------------------------
# Title Section
# -----------------------------
st.title("♻️ ReGenesis – Feasibility Intelligence Engine")
st.markdown("### Layer 1: Opportunity & Feasibility Analysis")

st.divider()

# -----------------------------
# User Input Section
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    waste_type = st.selectbox(
        "Select Waste Type",
        market_df["material_category"].unique()
    )

with col2:
    quantity = st.number_input(
        "Enter Quantity (kg)",
        min_value=1,
        step=10
    )

with col3:
    country = st.selectbox(
        "Select Country",
        country_df["country"]
    )

st.divider()

# -----------------------------
# Fetch Values
# -----------------------------
row = market_df[market_df["category"] == waste_type].iloc[0]

price_usd = row["avg_price_per_kg_usd"]
demand_score = row["demand_score_1_to_10"]

mismanaged = country_df[country_df["country"] == country]["mismanaged"].values[0]

# Convert USD to INR (approx)
price_inr = price_usd * 80

# -----------------------------
# Calculations
# -----------------------------
market_value = quantity * price_inr

market_strength = price_usd * demand_score
env_score = mismanaged / 20
scale_factor = quantity / 100

dfs_raw = market_strength * env_score * scale_factor
feasibility_score = min(100, dfs_raw * 10)

# -----------------------------
# Score Category
# -----------------------------
if feasibility_score < 30:
    status = "🔴 High Risk"
elif feasibility_score < 70:
    status = "🟡 Moderate Opportunity"
else:
    status = "🟢 High Potential"

# -----------------------------
# Output Dashboard
# -----------------------------
st.subheader("📊 Opportunity Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("💰 Market Value (₹)", f"{round(market_value, 2):,}")
c2.metric("🌍 Mismanaged Index", round(mismanaged, 2))
c3.metric("📈 Feasibility Score", round(feasibility_score, 2))

st.markdown(f"### Status: {status}")

st.divider()

# -----------------------------
# Explanation Section
# -----------------------------
with st.expander("ℹ️ How Feasibility Score Works"):
    st.write("""
    The Feasibility Score combines:
    - Market price & demand
    - Environmental pressure (mismanaged waste)
    - Production scale
    
    It predicts how viable a circular waste-based business is in the selected country.
    """)

st.caption("ReGenesis – Circular Economy Intelligence | Layer 1 MVP")
