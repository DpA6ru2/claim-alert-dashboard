import streamlit as st
import pandas as pd

st.set_page_config(page_title="Claim Deadline Dashboard", layout="wide")

st.title("🏠 Property Claim Deadline Tracker")
st.markdown("Monitor upcoming deadlines for tax sale claims and outreach status.")

# Sample data — replace with Supabase or API call later
data = {
    "Parcel ID": ["123-456-789", "987-654-321"],
    "Address": ["100 Main St, San Juan Capistrano", "200 Ocean Ave, Dana Point"],
    "Auction Date": ["2024-09-01", "2024-10-15"],
    "Claim Deadline": ["2025-09-01", "2025-10-15"],
    "Status": ["Unclaimed", "Filed"]
}

df = pd.DataFrame(data)

# Filters
status_filter = st.selectbox("Filter by Status", ["All", "Unclaimed", "Filed"])
if status_filter != "All":
    df = df[df["Status"] == status_filter]

# Display
st.dataframe(df, use_container_width=True)

# Optional: Add map or outreach queue later
