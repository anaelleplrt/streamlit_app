import streamlit as st
from utils.io import load_data, get_data_info
from utils.prep import clean_data
from sections import intro, data_quality, overview

st.set_page_config(
    page_title="Student Depression Dashboard",
    layout="wide",
    page_icon="🧠"
)

# Load data
df_raw = load_data()
df_clean, removed_cols, col_mapping, cleaning_stats = clean_data(df_raw)

# Sidebar
with st.sidebar:
    st.header("🎯 Navigation")
    section = st.radio(
        "Select Section:",
        ["Introduction", "Data Quality", "Overview", "Deep Dive", "Conclusions"]
    )

# Main title
st.title("🧠 Student Depression Analysis Dashboard")
st.caption("Understanding Mental Health Patterns in Student Populations")
st.markdown("---")

# Display selected section
if section == "Introduction":
    intro.show()
elif section == "Data Quality":
    data_quality.show(df_raw, df_clean, removed_cols, col_mapping, cleaning_stats)
elif section == "Overview":
    overview.show(df_clean)
elif section == "Deep Dive":
    st.info("Deep Dive section - Coming soon!")
elif section == "Conclusions":
    st.info("Conclusions section - Coming soon!")