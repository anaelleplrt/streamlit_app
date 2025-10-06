"""
Data preparation and feature engineering utilities
Handles cleaning, validation, and table creation for dashboard
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Tuple


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the raw dataset
    
    Args:
        df: Raw DataFrame from CSV
        
    Returns:
        Cleaned DataFrame
    """
    df_clean = df.copy()
    
    # Convert numeric columns (CORRECT camelCase names)
    numeric_cols = ['poids1', 'poidsTot', 'txNonStand', 'txStandDir', 'txStandIndir',
                    'txStandDirModBB', 'txStandDirModBH', 'txStandIndirModBB', 'txStandIndirModBH']
    
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Handle missing values in critical columns
    critical_cols = ['varTauxLib', 'type']
    for col in critical_cols:
        if col in df_clean.columns:
            df_clean = df_clean.dropna(subset=[col])
    
    # Create year column if date exists
    if 'annee' in df_clean.columns:
        df_clean['year'] = pd.to_numeric(df_clean['annee'], errors='coerce')
    
    # Ensure string columns are strings
    string_cols = ['varTauxLib', 'type', 'varGroupage', 'valGroupage', 'varPartition', 'valPartition']
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str)
    
    return df_clean


def get_data_quality_report(df: pd.DataFrame) -> Dict:
    """
    Generate data quality report
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with quality metrics
    """
    report = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'missing_by_column': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
    }
    
    # Check for key columns (CORRECT camelCase)
    required_cols = ['varTauxLib', 'type', 'varGroupage', 'valGroupage', 'txStandDir']
    report['missing_required_cols'] = [col for col in required_cols if col not in df.columns]
    
    return report


def make_tables(df: pd.DataFrame, filters: Dict = None) -> Dict[str, pd.DataFrame]:
    """
    Create analysis-ready tables from cleaned data
    
    Args:
        df: Cleaned DataFrame
        filters: Dictionary of filter values (region, disease, etc.)
        
    Returns:
        Dictionary of prepared tables for different views
    """
    df_filtered = df.copy()
    
    # Apply filters if provided (CORRECT camelCase)
    if filters:
        if filters.get('regions'):
            df_filtered = df_filtered[
                (df_filtered['varPartition'] == 'FISC_REG_S') &
                (df_filtered['valPartition'].isin(filters['regions']))
            ]
        
        if filters.get('disease'):
            df_filtered = df_filtered[df_filtered['varTauxLib'] == filters['disease']]
        
        if filters.get('type'):
            df_filtered = df_filtered[df_filtered['type'] == filters['type']]
    
    tables = {}
    
    tables['by_income'] = create_income_table(df_filtered)
    tables['by_region'] = create_region_table(df_filtered)
    tables['by_education'] = create_education_table(df_filtered)
    tables['by_csp'] = create_csp_table(df_filtered)
    tables['by_demographics'] = create_demographics_table(df_filtered)
    
    if 'year' in df_filtered.columns:
        tables['timeseries'] = create_timeseries_table(df_filtered)
    else:
        tables['timeseries'] = pd.DataFrame()
    
    return tables


def create_income_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create table grouped by income decile"""
    income_df = df[
        (df['varGroupage'] == 'FISC_NIVVIEM_E2015_S_moy_10') &
        (df['valGroupage'].notna()) &
        (df['valGroupage'] != 'nan')
    ].copy()
    
    if income_df.empty:
        return pd.DataFrame()
    
    income_df['income_decile'] = pd.to_numeric(income_df['valGroupage'], errors='coerce')
    income_df = income_df[income_df['income_decile'].notna()]
    
    # CORRECT column names
    agg_dict = {'txStandDir': 'mean'}
    
    if 'txStandDirModBB' in income_df.columns:
        agg_dict['txStandDirModBB'] = 'mean'
    if 'txStandDirModBH' in income_df.columns:
        agg_dict['txStandDirModBH'] = 'mean'
    if 'poids1' in income_df.columns:
        agg_dict['poids1'] = 'sum'
    
    agg_df = income_df.groupby(['income_decile', 'varTauxLib', 'type']).agg(agg_dict).reset_index()
    agg_df = agg_df.sort_values('income_decile')
    
    return agg_df


def create_region_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create table grouped by region"""
    region_df = df[
        (df['varGroupage'] == 'FISC_REG_S') &
        (df['valGroupage'].notna()) &
        (df['valGroupage'] != 'nan')
    ].copy()
    
    if region_df.empty:
        return pd.DataFrame()
    
    agg_dict = {'txStandDir': 'mean'}
    
    if 'txStandDirModBB' in region_df.columns:
        agg_dict['txStandDirModBB'] = 'mean'
    if 'txStandDirModBH' in region_df.columns:
        agg_dict['txStandDirModBH'] = 'mean'
    if 'poids1' in region_df.columns:
        agg_dict['poids1'] = 'sum'
    
    agg_df = region_df.groupby(['valGroupage', 'varTauxLib', 'type']).agg(agg_dict).reset_index()
    agg_df.rename(columns={'valGroupage': 'region_code'}, inplace=True)
    
    return agg_df


def create_education_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create table grouped by education level"""
    edu_df = df[
        (df['varGroupage'] == 'EAR_DIPLR_S') &
        (df['valGroupage'].notna()) &
        (df['valGroupage'] != 'nan')
    ].copy()
    
    if edu_df.empty:
        return pd.DataFrame()
    
    agg_dict = {'txStandDir': 'mean'}
    
    if 'txStandDirModBB' in edu_df.columns:
        agg_dict['txStandDirModBB'] = 'mean'
    if 'txStandDirModBH' in edu_df.columns:
        agg_dict['txStandDirModBH'] = 'mean'
    if 'poids1' in edu_df.columns:
        agg_dict['poids1'] = 'sum'
    
    agg_df = edu_df.groupby(['valGroupage', 'varTauxLib', 'type']).agg(agg_dict).reset_index()
    agg_df.rename(columns={'valGroupage': 'education_level'}, inplace=True)
    
    return agg_df


def create_csp_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create table grouped by socio-professional category"""
    csp_df = df[
        (df['varGroupage'] == 'EAR_GS_S') &
        (df['valGroupage'].notna()) &
        (df['valGroupage'] != 'nan')
    ].copy()
    
    if csp_df.empty:
        return pd.DataFrame()
    
    agg_dict = {'txStandDir': 'mean'}
    
    if 'txStandDirModBB' in csp_df.columns:
        agg_dict['txStandDirModBB'] = 'mean'
    if 'txStandDirModBH' in csp_df.columns:
        agg_dict['txStandDirModBH'] = 'mean'
    if 'poids1' in csp_df.columns:
        agg_dict['poids1'] = 'sum'
    
    agg_df = csp_df.groupby(['valGroupage', 'varTauxLib', 'type']).agg(agg_dict).reset_index()
    agg_df.rename(columns={'valGroupage': 'csp_group'}, inplace=True)
    
    return agg_df


def create_demographics_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create table with age and gender breakdown"""
    demo_df = df[
        ((df['varGroupage'] == 'classeAge10') | (df['varGroupage'] == 'SEXE')) &
        (df['valGroupage'].notna()) &
        (df['valGroupage'] != 'nan')
    ].copy()
    
    if demo_df.empty:
        return pd.DataFrame()
    
    agg_dict = {'txStandDir': 'mean'}
    
    if 'poids1' in demo_df.columns:
        agg_dict['poids1'] = 'sum'
    
    agg_df = demo_df.groupby(['varGroupage', 'valGroupage', 'varTauxLib', 'type']).agg(agg_dict).reset_index()
    
    return agg_df


def create_timeseries_table(df: pd.DataFrame) -> pd.DataFrame:
    """Create time series table if temporal data exists"""
    if 'year' not in df.columns:
        return pd.DataFrame()
    
    ts_df = df[df['year'].notna()].copy()
    
    if ts_df.empty:
        return pd.DataFrame()
    
    agg_dict = {'txStandDir': 'mean'}
    
    if 'poids1' in ts_df.columns:
        agg_dict['poids1'] = 'sum'
    
    agg_df = ts_df.groupby(['year', 'varTauxLib', 'type']).agg(agg_dict).reset_index()
    agg_df = agg_df.sort_values('year')
    
    return agg_df


def calculate_inequality_ratio(df: pd.DataFrame, disease: str, type_: str = 'prevalence') -> float:
    """
    Calculate inequality ratio: D1 (poorest) / D10 (richest)
    
    Args:
        df: Income table
        disease: Disease name
        type_: 'prevalence' or 'incidence'
        
    Returns:
        Ratio (higher = more inequality)
    """
    if df.empty:
        return np.nan
    
    filtered = df[
        (df['varTauxLib'] == disease) &
        (df['type'] == type_)
    ]
    
    if filtered.empty or 'income_decile' not in filtered.columns:
        return np.nan
    
    d1 = filtered[filtered['income_decile'] == 1]['txStandDir'].values
    d10 = filtered[filtered['income_decile'] == 10]['txStandDir'].values
    
    if len(d1) > 0 and len(d10) > 0 and d10[0] != 0:
        return d1[0] / d10[0]
    
    return np.nan


def get_top_diseases(df: pd.DataFrame, n: int = 10, by: str = 'prevalence') -> List[str]:
    """
    Get top N diseases by prevalence or incidence
    
    Args:
        df: Main DataFrame
        n: Number of diseases to return
        by: 'prevalence' or 'incidence'
        
    Returns:
        List of disease names
    """
    if df.empty:
        return []
    
    disease_data = df[df['type'] == by].copy()
    
    if disease_data.empty:
        return []
    
    disease_rates = disease_data.groupby('varTauxLib').agg({
        'txStandDir': 'mean'
    }).reset_index()
    
    disease_rates = disease_rates.sort_values('txStandDir', ascending=False)
    
    return disease_rates.head(n)['varTauxLib'].tolist()