import streamlit as st
import pandas as pd

st.set_page_config(page_title="ReGenesis", page_icon="♻️", layout="wide")

# ------------------------------------
# Load Data
# ------------------------------------
@st.cache_data
def load_data():

    market_df = pd.read_csv("plastic_market_prices.csv")

    raw_country = pd.read_excel("country_data.xlsx")

    # Auto pick first two columns
    country_df = raw_country.iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]

    country_df["country"] = country_df["country"].astype(str).str.lower().str.strip()
    country_df["mismanaged"] = pd.to_numeric(country_df["mismanaged"], errors="coerce")

    # Drop empty rows
    country_df = country_df.dropna()

    return market_df, country_df


market_df, country_df = load_data()

# ------------------------------------
# Header
# ------------------------------------
st.title("♻️ ReGenesis – Feasibility Intelligence Engine")
st.markdown("### Layer 1: Opportunity & Feasibility Analysis")

st.divider()

# ------------------------------------
# Inputs
# ------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    waste_type = st.selectbox(
        "Select Waste Type",
        market_df["category"].dropna().unique()
    )

with col2:
    quantity = st.number_input("Enter Quantity (kg)", min_value=1, value=10)

with col3:
    if len(country_df) == 0:
        st.error("Country dataset empty!")
        st.stop()

    country = st.selectbox("Select Country", sorted(country_df["country"].unique()))

# ------------------------------------
# Market Data
# ------------------------------------
row = market_df[market_df["category"] == waste_type].iloc[0]

price_usd = float(row["avg_price_per_kg_usd"])
demand = float(row["demand_score_1_to_10"])

# ------------------------------------
# Country Data SAFE
# ------------------------------------
match = country_df[country_df["country"] == country]

if match.empty:
    mismanaged = 1
else:
    mismanaged = float(match.iloc[0]["mismanaged"])

# ------------------------------------
# Calculations
# ------------------------------------
market_value = quantity * price_usd * 80

env_factor = mismanaged / country_df["mismanaged"].max()
scale = quantity / 100

score = price_usd * demand * env_factor * scale
feasibility = round(min(100, score * 10), 2)

# ------------------------------------
# Status
# ------------------------------------
if feasibility < 30:
    status = "🔴 High Risk"
elif feasibility < 70:
    status = "🟡 Moderate"
else:
    status = "🟢 High Potential"

# ------------------------------------
# Dashboard
# ------------------------------------
st.subheader("📊 Opportunity Dashboard")

a,b,c = st.columns(3)

a.metric("💰 Market Value ₹", round(market_value,2))
b.metric("🌍 Mismanaged Index", round(mismanaged,2))
c.metric("📈 Feasibility Score", feasibility)

st.markdown(f"## {status}")

# ------------------------------------
with st.expander("How score works"):
    st.write("""
Market Price  
Demand  
Environmental Pressure  
Production Scale  
""")

st.caption("ReGenesis | Layer 1 MVP")
