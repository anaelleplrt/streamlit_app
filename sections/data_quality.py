import pandas as pd
import streamlit as st

def check_missing_values(df):
    """
    Check for missing values in the dataset
    
    Args:
        df: DataFrame
        
    Returns:
        pd.DataFrame: Missing values summary
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percentage': missing_pct.values
    })
    
    # Only show columns with missing values
    missing_df = missing_df[missing_df['Missing_Count'] > 0]
    
    return missing_df


def check_duplicates(df):
    """
    Check for duplicate rows
    
    Args:
        df: DataFrame
        
    Returns:
        int: Number of duplicate rows
    """
    duplicates = df.duplicated().sum()
    return duplicates


def get_column_descriptions():
    """
    Return descriptions of all columns in the dataset
    
    Returns:
        dict: Column names and their descriptions
    """
    descriptions = {
        'id': 'Unique identifier for each student',
        'Gender': 'Student gender (Male/Female)',
        'Age': 'Student age in years',
        'City': 'City where student lives',
        'Profession': 'Student occupation (constant: all "Student")',
        'Academic_Pressure': 'Level of academic stress (scale 1-5)',
        'Work_Pressure': 'Level of work-related stress (constant: all 0)',
        'CGPA': 'Cumulative Grade Point Average (scale 0-10)',
        'Study_Satisfaction': 'Satisfaction with studies (scale 1-5)',
        'Job_Satisfaction': 'Job satisfaction level (constant: all 0)',
        'Sleep_Duration': 'Hours of sleep per night (categorical)',
        'Dietary_Habits': 'Quality of diet (Healthy/Moderate/Unhealthy)',
        'Degree': 'Type of degree pursuing (BA, BSc, etc.)',
        'Suicidal_Thoughts': 'History of suicidal ideation (Yes/No)',
        'Work_Study_Hours': 'Total hours spent on work/study per day',
        'Financial_Stress': 'Level of financial stress (scale 1-5)',
        'Family_History_Mental_Illness': 'Family history of mental health issues (Yes/No)',
        'Depression': 'Depression status (0=No, 1=Yes) - TARGET VARIABLE'
    }
    return descriptions


def validate_numeric_ranges(df):
    """
    Validate that numeric columns are within expected ranges
    
    Args:
        df: DataFrame
        
    Returns:
        dict: Validation results
    """
    validations = {}
    
    # Age: should be reasonable for students
    if 'Age' in df.columns:
        validations['age'] = {
            'min': df['Age'].min(),
            'max': df['Age'].max(),
            'valid': (df['Age'] >= 18).all() and (df['Age'] <= 100).all()
        }
    
    # CGPA: should be between 0-10
    if 'CGPA' in df.columns:
        validations['cgpa'] = {
            'min': df['CGPA'].min(),
            'max': df['CGPA'].max(),
            'valid': (df['CGPA'] >= 0).all() and (df['CGPA'] <= 10).all()
        }
    
    # Pressure scores: should be between 0-5
    if 'Academic_Pressure' in df.columns:
        validations['academic_pressure'] = {
            'min': df['Academic_Pressure'].min(),
            'max': df['Academic_Pressure'].max(),
            'valid': (df['Academic_Pressure'] >= 0).all() and (df['Academic_Pressure'] <= 5).all()
        }
    
    return validations


def show_column_info(df):
    """
    Display detailed information about each column
    
    Args:
        df: DataFrame
    """
    st.markdown("### 📋 Dataset Columns Information")
    
    descriptions = get_column_descriptions()
    
    # Create DataFrame with column info
    col_info = []
    for col in df.columns:
        col_info.append({
            'Column Name': col,
            'Data Type': str(df[col].dtype),
            'Non-Null Count': df[col].notna().sum(),
            'Unique Values': df[col].nunique(),
            'Description': descriptions.get(col, 'No description available')
        })
    
    col_df = pd.DataFrame(col_info)
    st.dataframe(col_df, use_container_width=True, hide_index=True)


def show_cleaning_summary(removed_columns, column_mapping, cleaning_stats, df_raw):
    """
    Display detailed summary of data cleaning actions
    
    Args:
        removed_columns: List of removed column names
        column_mapping: Dictionary of renamed columns
        cleaning_stats: Dictionary with cleaning statistics
        df_raw: Original DataFrame to check column values
    """
    st.markdown("### 🧹 Data Cleaning Process")
    
    st.markdown("""
    The following cleaning steps were applied to ensure data quality and follow best practices:
    """)
    
    # Step 0: Column renaming
    st.markdown("#### 0️⃣ Standardizing Column Names")
    if column_mapping:
        st.write(f"**Renamed {len(column_mapping)} columns** to follow `snake_case` convention:")
        
        with st.expander("View renamed columns"):
            rename_df = pd.DataFrame({
                'Original Name': list(column_mapping.keys()),
                'New Name': list(column_mapping.values())
            })
            st.dataframe(rename_df, use_container_width=True, hide_index=True)
        
        st.write("""
        **Why rename columns?**
        - Remove spaces and special characters (?, !)
        - Follow Python naming conventions (snake_case)
        - Easier to use in code and analysis
        - Improve readability and consistency
        """)
    
    # Step 1: Missing values
    st.markdown("#### 1️⃣ Handling Missing Values")
    rows_removed_missing = cleaning_stats.get('rows_removed_missing', 0)
    if rows_removed_missing > 0:
        st.write(f"- **Action**: Removed **{rows_removed_missing} rows** with missing values")
        st.write(f"- **Reason**: Only {rows_removed_missing} missing values ({rows_removed_missing/len(df_raw)*100:.3f}%) - minimal impact on dataset")
        st.write(f"- **Column affected**: Financial_Stress")
    else:
        st.success("✅ No missing values found")
    
    # Step 2: City filtering
    st.markdown("#### 2️⃣ Filtering Cities by Sample Size")
    
    cities_removed = cleaning_stats.get('cities_removed', 0)
    rows_removed_city = cleaning_stats.get('rows_removed_city', 0)
    min_threshold = cleaning_stats.get('min_students_threshold', 20)
    
    if cities_removed > 0:
        st.warning(f"**Removed {cities_removed} cities** with fewer than {min_threshold} students")
        st.write(f"- **Rows affected**: {rows_removed_city:,} students removed ({rows_removed_city/len(df_raw)*100:.2f}% of dataset)")
        st.write(f"- **Threshold**: Minimum {min_threshold} students per city")
        
        st.write(f"""
        **Why filter by city size?**
        - **Statistical validity**: Small samples (1-19 students) produce unreliable percentages
        - **Data quality**: Removes suspicious city names (e.g., "3.0", "M.Com", "City")
        - **Bias reduction**: Prevents outliers from skewing geographic analysis
        - **Focus on meaningful data**: Concentrates analysis on well-represented cities
        
        **Examples of issues with small cities:**
        - 1 student with depression = 100% depression rate (misleading)
        - Invalid city names suggest data entry errors
        - Cannot make reliable geographic comparisons
        """)
    else:
        st.success("✅ All cities meet minimum sample size threshold")
    
    # Step 3: Constant columns
    st.markdown("#### 3️⃣ Removing Constant Columns")
    
    if removed_columns:
        st.warning(f"**Removed {len(removed_columns)} column(s)** that contain only constant values:")
        
        for col in removed_columns:
            # Check if column exists in raw data with old name
            original_col = col
            for old_name, new_name in column_mapping.items():
                if new_name == col and old_name in df_raw.columns:
                    original_col = old_name
                    break
            
            if original_col in df_raw.columns:
                unique_val = df_raw[original_col].unique()[0]
            else:
                unique_val = "N/A"
            
            st.write(f"- **`{col}`**: All values = `{unique_val}`")
        
        st.write("""
        **Why remove these columns?**
        - No variation = no analytical value
        - Cannot be used for comparisons or correlations
        - Improves performance and clarity
        """)
    else:
        st.success("✅ No constant columns found")
    
    # Step 4: Data type verification
    st.markdown("#### 4️⃣ Data Type Verification")
    st.write("""
    - **Depression**: Ensured integer type (0 or 1) for binary classification
    - **Numeric columns**: Validated ranges (Age, CGPA, Pressure scores)
    - **Categorical columns**: Preserved as strings (Gender, City, Degree, etc.)
    """)


def show(df_raw, df_clean, removed_columns, column_mapping, cleaning_stats):
    """
    Display complete data quality section
    
    Args:
        df_raw: Original DataFrame
        df_clean: Cleaned DataFrame
        removed_columns: List of removed column names
        column_mapping: Dictionary of renamed columns
        cleaning_stats: Dictionary with cleaning statistics
    """
    st.markdown("## 📊 Data Quality & Validation")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    missing_count = df_raw.isnull().sum().sum()
    missing_pct = (missing_count / (len(df_raw) * len(df_raw.columns))) * 100
    duplicates = check_duplicates(df_raw)
    total_removed = len(df_raw) - len(df_clean)
    
    col1.metric("Original Records", f"{len(df_raw):,}")
    col2.metric("Final Records", f"{len(df_clean):,}")
    col3.metric("Records Removed", f"{total_removed:,}", delta=f"-{total_removed/len(df_raw)*100:.1f}%")
    col4.metric("Columns Renamed", len(column_mapping))
    
    st.markdown("---")
    
    # Detailed cleaning summary
    show_cleaning_summary(removed_columns, column_mapping, cleaning_stats, df_raw)
    
    st.markdown("---")
    
    # Column information
    show_column_info(df_clean)
    
    st.markdown("---")
    
    # Missing values details (if any)
    if missing_count > 0:
        st.markdown("### 🔍 Missing Values Details")
        missing_df = check_missing_values(df_raw)
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Validation checks
    st.markdown("### ✅ Data Validation Checks")
    validations = validate_numeric_ranges(df_clean)
    
    all_valid = all(v['valid'] for v in validations.values())
    
    if all_valid:
        st.success("✅ All numeric values are within expected ranges")
    else:
        st.warning("⚠️ Some values may be outside expected ranges")
    
    with st.expander("View validation details"):
        for field, result in validations.items():
            st.write(f"**{field.replace('_', ' ').title()}**: "
                    f"Range [{result['min']:.2f} - {result['max']:.2f}] "
                    f"{'✅' if result['valid'] else '❌'}")
    
    st.markdown("---")
    
    # Limitations
    st.markdown("### ⚠️ Important Limitations")
    st.info("""
    **Data Collection:**
    - Self-reported data (potential response bias)
    - Cross-sectional snapshot (not longitudinal study)
    - Anonymized dataset from Kaggle
    
    **Data Quality & Cleaning:**
    - Removed cities with <20 students for statistical validity
    - Some city names were suspicious (numeric values, invalid entries)
    - Geographic coverage limited to well-represented Indian cities
    
    **Representativeness:**
    - Sample focuses on cities with sufficient data
    - May not represent all student populations or small towns
    - Cultural and socioeconomic factors not fully captured
    
    **Usage Notes:**
    - This analysis is for educational purposes only
    - Results should not be used for individual diagnosis
    - Patterns shown are correlational, not causal
    """)