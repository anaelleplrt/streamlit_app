# utils/prep.py
import pandas as pd

# Exclude EU/EZ aggregates from the country filter (not actual countries)
EXCLUDE_CODES = {"EA", "EA18", "EA19", "EA20", "EU", "EU27_2007", "EU27_2020", "EU28"}

# Order for age buckets in the UI
AGE_BUCKET_ORDER = ["Total", "<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "≥75"]
AGE_IDX = {v: i for i, v in enumerate(AGE_BUCKET_ORDER)}

def get_filter_defaults(df: pd.DataFrame):
    # Countries (ISO-2), excluding aggregates
    geo_all = sorted(df["geo"].dropna().unique()) if "geo" in df.columns else []
    geo_all = [g for g in geo_all if g not in EXCLUDE_CODES]

    # Years
    years_all = sorted(int(y) for y in df["year"].dropna().unique()) if "year" in df.columns else []

    # Gender
    sex_all = sorted(df["sex_label"].dropna().unique()) if "sex_label" in df.columns else ["Total"]

    # Age buckets present in data, ordered logically
    if "age_bucket_label" in df.columns:
        present = sorted(df["age_bucket_label"].dropna().unique(), key=lambda x: AGE_IDX.get(x, 999))
        if "Total" in present:
            present = ["Total"] + [x for x in present if x != "Total"]
        age_all = present if present else ["Total"]
    else:
        age_all = ["Total"]

    # Income groups
    inc_all = sorted(df["incgrp_label"].dropna().unique()) if "incgrp_label" in df.columns else ["Total"]

    return {
        "geo_all": geo_all,
        "geo_default": [g for g in ["FR", "DE", "IT", "ES", "PL"] if g in geo_all],
        "years_all": years_all,
        "sex_all": sex_all,
        "sex_default_idx": sex_all.index("Total") if "Total" in sex_all else 0,
        "age_all": age_all,
        "age_default_idx": age_all.index("Total") if "Total" in age_all else 0,
        "inc_all": inc_all,
        "inc_default_idx": inc_all.index("Total") if "Total" in inc_all else 0,
    }

def apply_filters(df: pd.DataFrame, f: dict) -> pd.DataFrame:
    out = df.copy()
    if f.get("geo"):
        out = out[out["geo"].isin(f["geo"])]
    if f.get("sex"):
        out = out[out["sex_label"] == f["sex"]]
    if f.get("age"):
        col = "age_bucket_label" if "age_bucket_label" in out.columns else "age_label"
        out = out[out[col] == f["age"]]
    if f.get("inc"):
        out = out[out["incgrp_label"] == f["inc"]]
    return out

def build_tables(df: pd.DataFrame) -> dict:
    t = {}
    if {"geo", "year", "obs_value"}.issubset(df.columns):
        t["timeseries"] = (
            df.groupby(["geo", "year"], as_index=False)["obs_value"].mean()
            .sort_values(["geo", "year"])
        )
    if {"geo", "iso3", "year", "obs_value"}.issubset(df.columns):
        last_year = int
