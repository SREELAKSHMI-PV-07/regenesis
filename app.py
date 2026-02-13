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

    country_df["mismanaged"] = (
        country_df["mismanaged"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
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
    mismanaged = 5
else:
    mismanaged = float(match["mismanaged"].values[0])

# ---------------- INTEGRATED MODEL ----------------

price_inr = price_usd * 80
market_value = quantity * price_inr

scale_factor = 1 + (quantity / 500)
mismanaged_factor = 1 + (mismanaged / 100 * 5)

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
c2.metric("🌍 Mismanaged Waste", round(mismanaged, 2))
c3.metric("📦 Scale Multiplier", round(scale_factor, 2))
c4.metric("📈 Feasibility Score", feasibility_score)

st.markdown(f"### Status: {status}")

# ---------------- FEASIBILITY EXPLANATION (NOW BELOW STATUS) ----------------
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

All factors integrate to estimate circular business feasibility.
""")

st.caption("ReGenesis – Circular Economy Intelligence | Layer 1 MVP")
