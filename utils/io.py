import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Load the Student Depression Dataset
    
    Returns:
        pd.DataFrame: Raw dataset
    """
    df = pd.read_csv('data/Student Depression Dataset.csv')
    return df

def get_data_info(df):
    """
    Return basic information about the dataset
    
    Args:
        df: DataFrame
        
    Returns:
        dict: Dictionary with statistics
    """
    info = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'depression_rate': (df['Depression'].sum() / len(df)) * 100
    }
    return info