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

match = country_df[country_df["country"].str.contains(country, case=False, na=False)]

if match.empty:
    mismanaged = 0.5
else:
    mismanaged = float(match.iloc[0]["mismanaged"])

# ---------------- Calculations ----------------

# ---------------- Calculations ----------------

price_inr = price_usd * 80
market_value = quantity * price_inr

# Normalize factors
market_factor = (price_usd * demand_score) / 10
env_factor = mismanaged / 100   # assume mismanaged is percentage
scale_factor = quantity / 100

raw_score = market_factor * env_factor * scale_factor

# Smooth scaling using sigmoid-like cap
feasibility_score = round((raw_score / (raw_score + 1)) * 100, 2)

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
