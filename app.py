# app.py — Eurostat Clothing Deprivation Dashboard (multipage)
import streamlit as st
import pandas as pd

from utils.io import load_eurostat_csv
from utils.prep import build_tables, get_filter_defaults, apply_filters
from sections import intro, overview, deep_dives, conclusions

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Clothing Deprivation in Europe (Eurostat)", layout="wide")

# ---------- SIDEBAR: CACHE RESET ----------
with st.sidebar:
    if st.button("🔄 Reload data (clear cache)"):
        st.cache_data.clear()
        st.rerun()

# ---------- DATA ----------
@st.cache_data(show_spinner=True)
def get_data():
    df = load_eurostat_csv("data/eurostat_clothes.csv")
    tables = build_tables(df)
    return df, tables

df_raw, tables = get_data()

# ---------- SIDEBAR: NAVIGATION & FILTERS ----------
with st.sidebar:
    st.image("assets/logo.png", use_container_width=True) if False else None
    st.header("Navigation")
    page = st.radio(
        "Go to:",
        ["Introduction", "Overview", "Detailed Analyses", "Conclusions"],
        index=1
    )

    st.header("Filters")
    defaults = get_filter_defaults(df_raw)

    # ---- COUNTRY FILTER WITH "SELECT ALL" OPTION ----
    all_countries = defaults["geo_all"]
    select_all = st.checkbox("Select all countries", value=True)
    if select_all:
        geo = st.multiselect("Countries (ISO-2)", all_countries, default=all_countries)
    else:
        geo = st.multiselect("Countries (ISO-2)", all_countries, default=defaults["geo_default"])

    sex = st.selectbox("Gender", defaults["sex_all"], index=defaults["sex_default_idx"])
    age = st.selectbox("Age group", defaults["age_all"], index=defaults["age_default_idx"])
    inc = st.selectbox("Income group", defaults["inc_all"], index=defaults["inc_default_idx"])
    years = defaults["years_all"]
    year_for_map = st.selectbox(
        "Year (map & ranking)",
        years,
        index=len(years) - 1 if years else 0
    )

filters = {
    "geo": geo,
    "sex": sex,
    "age": age,
    "inc": inc,
    "year_for_map": year_for_map,
}

# Filtered data (applied once here, reused by all sections)
df_sel = apply_filters(df_raw, filters)

# ---------- HEADER ----------
st.title("Clothing Deprivation in Europe")
st.caption(
    "Source: Eurostat — *Persons who cannot afford to replace worn-out clothes by some new (not second-hand) ones "
    "by age, sex and income group* (unit: %)."
)

# ---------- PAGE ROUTING ----------
if page == "Introduction":
    intro.render(df_raw, tables, filters)
elif page == "Overview":
    overview.render(df_sel, tables, filters)
elif page == "Detailed Analyses":
    deep_dives.render(df_raw, tables, filters)
else:
    conclusions.render(df_sel, tables, filters)
