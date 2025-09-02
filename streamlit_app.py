import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# --- Supabase Setup ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Page Config ---
st.set_page_config(page_title="Riverside Claim Dashboard", layout="wide")
st.title("🏠 Riverside County Tax Overages Dashboard")
st.markdown("Track unclaimed excess proceeds from tax-defaulted property sales.")

# --- Load Data from Supabase ---
try:
    response = supabase.table("overages_riverside").select("*").execute()
    df = pd.DataFrame(response.data)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# --- Data Cleanup ---
for col in ["overage_amount", "minimum_bid", "sale_price"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Claim Deadline Countdown ---
def calculate_days_left(deadline):
    try:
        return (datetime.strptime(deadline, "%Y-%m-%d") - datetime.today()).days
    except:
        return None

df["days_left"] = df["claim_deadline"].apply(calculate_days_left)

# --- Filters ---
with st.sidebar:
    st.header("🔍 Filters")
    city_filter = st.selectbox("City", ["All"] + sorted(df["city"].dropna().unique()))
    min_overage = st.slider("Minimum Overage ($)", 0, int(df["overage_amount"].max()), 50000)
    deadline_filter = st.checkbox("Show only claims expiring in < 30 days")

# --- Apply Filters ---
if city_filter != "All":
    df = df[df["city"] == city_filter]
df = df[df["overage_amount"] >= min_overage]
if deadline_filter:
    df = df[df["days_left"].notnull() & (df["days_left"] < 30)]

# --- Display Dashboard ---
st.subheader("📋 Unclaimed Overages")
st.dataframe(
    df[["apn", "address", "city", "zip", "overage_amount", "claim_deadline", "days_left", "status"]],
    use_container_width=True
)

# --- Outreach Tracker ---
st.subheader("📣 Outreach Status")
status_counts = df["status"].value_counts()
st.bar_chart(status_counts)

# --- Export Option ---
st.download_button("Download Filtered Data", df.to_csv(index=False), "riverside_overages.csv")
