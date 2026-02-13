import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ReGenesis – Layer 1",
    page_icon="♻️",
    layout="wide"
)

@st.cache_data
def load_data():
    market_df = pd.read_csv("plastic_market_prices.csv")

    country_df = pd.read_excel("country_data.xlsx").iloc[:, :2]
    country_df.columns = ["country", "mismanaged"]

    # Clean + force numeric
    country_df["country"] = country_df["country"].astype(str).str.lower().str.strip()
    country_df["mismanaged"] = pd.to_numeric(country_df["mismanaged"], errors="coerce")

    return market_df, country_df


market_df, country_df = load_data()

st.title("♻️ ReGenesis – Feasibility Intelligence Engine")
st.markdown("### Layer 1: Opportunity & Feasibility Analysis")

st.divider()

# ---------------- Inputs ----------------

col1, col2, col3 = st.columns(3)

with col1:
    waste_type = st.selectbox("Select Waste Type", market_df["category"].unique())

with col2:
    quantity = st.number_input("Enter Quantity (kg)", min_value=1, step=1)

with col3:
    country_list = sorted(country_df["country"].dropna().unique())
    country = st.selectbox("Select Country", country_list)

st.divider()

# ---------------- Market Data ----------------

row = market_df[market_df["category"] == waste_type].iloc[0]

price_usd = float(row["avg_price_per_kg_usd"])
demand_score = float(row["demand_score_1_to_10"])

# ---------------- Country Data ----------------

mismanaged_val = country_df.loc[country_df["country"] == country, "mismanaged"].values

if len(mismanaged_val) == 0 or pd.isna(mismanaged_val[0]):
    mismanaged = 0.5
else:
    mismanaged = float(mismanaged_val[0])

# ---------------- Calculations ----------------

price_inr = price_usd * 80
market_value = quantity * price_inr

env_score = mismanaged / 10
scale_factor = quantity / 50

dfs = price_usd * demand_score * env_score * scale_factor

feasibility_score = round(min(100, dfs * 10), 2)

# ---------------- Status ----------------

if feasibility_score < 30:
    status = "🔴 High Risk"
elif feasibility_score < 70:
    status = "🟡 Moderate Opportunity"
else:
    status = "🟢 High Potential"

# ---------------- Dashboard ----------------

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

Used to estimate circular business feasibility.
""")

st.caption("ReGenesis – Circular Economy Intelligence | Layer 1 MVP")
