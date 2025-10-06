# utils/io.py
import pandas as pd
import re

# -------- Age bucketing --------
def _age_to_bucket_label(age_code_or_label: str) -> str:
    """
    Regroupe tous les codes Eurostat d'âge en 9 buckets standard:
    Total, <18, 18-24, 25-34, 35-44, 45-54, 55-64, 65-74, ≥75
    """
    if not isinstance(age_code_or_label, str):
        return "Total"

    s = age_code_or_label.strip().upper()

    # Total
    if s in {"TOTAL", "T"}:
        return "Total"

    # Cas explicites
    if s in {"Y_LT18", "LT18", "<18"}:
        return "<18"
    if s in {"Y_GE75", "GE75", ">=75", "≥75"}:
        return "≥75"

    # Ranges "Y18-24", "Y45-64", "18-64", etc.
    m = re.match(r"Y?(\d{1,2})\s*[-–]\s*(\d{1,2})", s)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if hi < 18:
            return "<18"
        if lo >= 75:
            return "≥75"
        # Choix du bucket dominant par la borne basse
        if lo < 18: return "<18"
        if lo < 25: return "18-24"
        if lo < 35: return "25-34"
        if lo < 45: return "35-44"
        if lo < 55: return "45-54"
        if lo < 65: return "55-64"
        if lo < 75: return "65-74"
        return "≥75"

    # Seuils "Y_GE16", "Y_GE18", "GE65", etc.
    m = re.match(r"Y?_?GE(\d{1,2})", s)
    if m:
        lo = int(m.group(1))
        if lo >= 75: return "≥75"
        if lo < 18:  return "<18"
        if lo < 25:  return "18-24"
        if lo < 35:  return "25-34"
        if lo < 45:  return "35-44"
        if lo < 55:  return "45-54"
        if lo < 65:  return "55-64"
        if lo < 75:  return "65-74"
        return "≥75"

    # Autres formes "Y18_24", "18 TO 24", "Y75_84"...
    nums = re.findall(r"\d{1,2}", s)
    if nums:
        lo = int(nums[0])
        if lo < 18: return "<18"
        if lo < 25: return "18-24"
        if lo < 35: return "25-34"
        if lo < 45: return "35-44"
        if lo < 55: return "45-54"
        if lo < 65: return "55-64"
        if lo < 75: return "65-74"
        return "≥75"

    return "Total"

def load_eurostat_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Garder seulement % (PC)
    if "unit" in df.columns:
        df = df[df["unit"].str.upper() == "PC"].copy()

    # Année & valeur
    if "time_period" in df.columns:
        df["year"] = pd.to_numeric(df["time_period"], errors="coerce").astype("Int64")
    df["obs_value"] = pd.to_numeric(df.get("obs_value"), errors="coerce")

    # Libellés
    sex_map = {"M": "Men", "F": "Women", "T": "Total"}
    if "sex" in df.columns:
        df["sex_label"] = df["sex"].map(sex_map).fillna(df["sex"])

    # Âge: on garde l'original + on crée le bucket
    if "age" in df.columns:
        df["age_label"] = df["age"].astype(str)
        df["age_bucket_label"] = df["age"].astype(str).apply(_age_to_bucket_label)

    # Groupe    
    inc_map = {
        "A_MD60": "≥ 60% of median income — non-poor",
        "B_MD60": "< 60% of median income — at-risk-of-poverty",
        "TOTAL":  "All the population"
    }
    if "incgrp" in df.columns:
        df["incgrp_label"] = df["incgrp"].str.upper().map(inc_map).fillna(df["incgrp"])


    # ISO2 -> ISO3 pour la carte
    iso2_to_iso3 = {
        "AL":"ALB","AT":"AUT","BE":"BEL","BG":"BGR","CH":"CHE","CY":"CYP","CZ":"CZE","DE":"DEU","DK":"DNK",
        "EE":"EST","EL":"GRC","ES":"ESP","FI":"FIN","FR":"FRA","HR":"HRV","HU":"HUN","IE":"IRL","IS":"ISL",
        "IT":"ITA","LI":"LIE","LT":"LTU","LU":"LUX","LV":"LVA","ME":"MNE","MK":"MKD","MT":"MLT","NL":"NLD",
        "NO":"NOR","PL":"POL","PT":"PRT","RO":"ROU","RS":"SRB","SE":"SWE","SI":"SVN","SK":"SVK","TR":"TUR",
        "UK":"GBR","GB":"GBR"
    }
    if "geo" in df.columns:
        df["iso3"] = df["geo"].str.upper().map(iso2_to_iso3)

    return df
