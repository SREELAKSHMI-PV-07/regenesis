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
    # Load market data
    market_df = pd.read_csv("plastic_market_prices.csv")
    market_df.columns = market_df.columns.str.strip()

    # Remove unwanted Excel index columns if any
    market_df = market_df.loc[:, ~market_df.columns.str.contains("^Unnamed")]

    # Load country data
    country_df = pd.read_excel("country_data.xlsx").iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]

    # Clean data
    country_df["country"] = (
        country_df["country"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    country_df["mismanaged"] = (
        country_df["mismanaged"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    country_df["mismanaged"] = pd.to_numeric(
        country_df["mismanaged"],
        errors="coerce"
    )

    # Remove empty rows
    country_df = country_df.dropna()
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
    country = st.selectbox("Select Country", country_list)

country = country.lower().strip()

st.divider()

# ---------------- MARKET DATA ----------------
row = market_df[market_df["category"] == waste_type].iloc[0]

price_usd = float(row["avg_price_per_kg_usd"])
demand_score = float(row["demand_score_1_to_10"])

# ---------------- COUNTRY MATCHING ----------------
match = country_df[
    country_df["country"].str.contains(country, case=False, na=False)
]

if match.empty:
    mismanaged = 5
else:
    mismanaged = float(match["mismanaged"].values[0])

# ---------------- INTEGRATED MODEL ----------------

# Revenue potential
price_inr = price_usd * 80
market_value = quantity * price_inr

# Scale multiplier
scale_factor = 1 + (quantity / 500)

# Environmental opportunity factor
mismanaged_factor = 1 + (mismanaged / 100 * 5)

# Feasibility calculation
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
c2.metric("🌍 Mismanaged Waste (%)", round(mismanaged,2))
c3.metric("📦 Scale Multiplier", round(scale_factor,2))
c4.metric("📈 Feasibility Score", feasibility_score)

st.markdown(f"### Status: {status}")

st.divider()

# ---------------- CLEAN DATA PREVIEW ----------------
with st.expander("📂 Cleaned Country Data (Preview)"):
    st.dataframe(country_df, hide_index=True)

# ---------------- INFO ----------------
with st.expander("ℹ️ How Feasibility Score Works"):
    st.write("""
• Market strength → Price × Demand  
• Scale efficiency → Larger quantities improve viability  
• Environmental pressure → Higher mismanaged waste increases opportunity  

All factors integrate to estimate circular business feasibility.
""")

st.caption("ReGenesis – Circular Economy Intelligence | Layer 1 MVP")
