"""
Data loading utilities for DREES ER 1243 dataset
Loads chronic diseases and social inequalities data from local CSV
"""

import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Optional

# License and attribution
LICENSE_TEXT = """
**Data Source:** DREES (Direction de la Recherche, des Études, de l'Évaluation et des Statistiques)  
**Dataset:** ER 1243 - Social Inequalities and Chronic Diseases  
**Publication:** "Chronic diseases affect modest people more often and reduce their life expectancy further"  
**License:** Open License / Licence Ouverte (Etalab)  
**URL:** https://data.drees.solidarites-sante.gouv.fr/
"""

# Variable label mappings (from documentation)
VARIABLE_LABELS = {
    'SEXE': 'Gender',
    'classeAge10': 'Age Group (10-year)',
    'FISC_REG_S': 'Region',
    'FISC_NIVVIEM_E2015_S_moy_10': 'Income Decile',
    'EAR_GS_S': 'Socio-Professional Group',
    'EAR_DIPLR_S': 'Education Level'
}

GENDER_LABELS = {
    '1': 'Male',
    '2': 'Female'
}

# Income decile labels (1=poorest, 10=richest)
INCOME_LABELS = {
    str(i): f"D{i} {'(Poorest)' if i==1 else '(Richest)' if i==10 else ''}"
    for i in range(1, 11)
}


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Load data from local CSV file
    
    Returns:
        DataFrame with raw data
    """
    # Construct path to data file
    csv_path = Path(__file__).parent.parent / "data" / "er_inegalites_maladies_chroniques.csv"
    
    if not csv_path.exists():
        st.error(f"Data file not found: {csv_path}")
        st.info("Please ensure 'er_inegalites_maladies_chroniques.csv' is in the data/ folder")
        return pd.DataFrame()
    
    try:
        # Load CSV with semicolon separator - CORRECT FORMAT
        df = pd.read_csv(csv_path, encoding='utf-8', low_memory=False, sep=';')
        
        st.sidebar.caption(f"Loaded {len(df):,} records with {len(df.columns)} columns")
        
        return df
        
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()


def get_license_info() -> str:
    """Return license and attribution text"""
    return LICENSE_TEXT


def get_variable_label(var_name: str, var_value: str = None) -> str:
    """
    Get human-readable label for variable name or value
    
    Args:
        var_name: Variable name (e.g., 'SEXE')
        var_value: Variable value (optional)
        
    Returns:
        Human-readable label
    """
    if var_value:
        if var_name == 'SEXE':
            return GENDER_LABELS.get(str(var_value), str(var_value))
        elif var_name == 'FISC_NIVVIEM_E2015_S_moy_10':
            return INCOME_LABELS.get(str(var_value), f"Decile {var_value}")
    
    return VARIABLE_LABELS.get(var_name, var_name)