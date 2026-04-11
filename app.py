import streamlit as st
import pandas as pd
from utils import calculate_score

st.set_page_config(page_title="AI Campaign Tool", layout="wide")

# LOGIN 
USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# MAIN 
st.title("AI Influencer Campaign Dashboard")

# UPLOAD 
st.subheader("📂 Upload Influencer Data")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data.csv")

# Column cleaning 
df.columns = df.columns.str.lower().str.strip()

df.rename(columns={
    "engagement_rate_%": "engagement",
    "avg_views": "views",
    "cost_per_post": "cost"
}, inplace=True)

# AI (Fake using primary niche) 
df["Detected_Niche"] = df["primary_niche"]

# SCORE 
df["Score"] = df.apply(
    lambda x: calculate_score(
        x["followers"],
        x["engagement"],
        x["views"],
        x["cost"]
    ),
    axis=1
)

#  FILTER 
st.sidebar.header("Filters")

niche_filter = st.sidebar.selectbox(
    "Select Niche",
    ["All"] + list(df["Detected_Niche"].unique())
)

if niche_filter != "All":
    df = df[df["Detected_Niche"] == niche_filter]

#  SORT 
df = df.sort_values(by="Score", ascending=False)

# TABLE 
st.subheader("Top Creators")
st.dataframe(df)

# DOWNLOAD 
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇ Download Report", csv, "report.csv", "text/csv")

#  CHART 
st.subheader("📈 Followers vs Engagement")
st.scatter_chart(df[["followers", "engagement"]])

# CAMPAIGN 
st.subheader("🎯 Create Campaign")

campaign_name = st.text_input("Campaign Name")
budget = st.number_input("Budget (₹)", min_value=1000)

selected_niche = st.selectbox(
    "Target Niche",
    df["Detected_Niche"].unique()
)

if st.button("Create Campaign"):
    st.success(f"Campaign '{campaign_name}' created for {selected_niche} with budget ₹{budget}")

# RECOMMENDATION 
st.subheader("AI Recommended Creators")

filtered_df = df[
    (df["Detected_Niche"] == selected_niche) &
    (df["cost"] <= budget)
]

if len(filtered_df) == 0:
    st.warning("No creators match your budget 😳")
else:
    recommended = filtered_df.sort_values(by="Score", ascending=False).head(3)
    st.dataframe(recommended)

# SHORTLIST
st.subheader("⭐ Shortlist Creators")

shortlist = st.multiselect("Select Creators", df["name"])

if st.button("Save Shortlist"):
    st.success(f"Shortlisted: {', '.join(shortlist)}")
    st.dataframe(df[df["name"].isin(shortlist)])