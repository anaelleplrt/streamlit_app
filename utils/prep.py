import pandas as pd

def clean_data(df):
    """
    Clean the dataset by:
    - Renaming columns to follow snake_case convention
    - Removing missing values
    - Removing cities with too few students (<20) for statistical validity
    - Removing constant/useless columns
    - Preparing data types
    
    Args:
        df: Raw DataFrame
        
    Returns:
        tuple: (Cleaned DataFrame, list of removed columns, dict of renamed columns, dict of cleaning stats)
    """
    # Step 1: Rename columns for consistency
    column_mapping = {
        'Have you ever had suicidal thoughts ?': 'Suicidal_Thoughts',
        'Family History of Mental Illness': 'Family_History_Mental_Illness',
        'Sleep Duration': 'Sleep_Duration',
        'Dietary Habits': 'Dietary_Habits',
        'Academic Pressure': 'Academic_Pressure',
        'Work Pressure': 'Work_Pressure',
        'Study Satisfaction': 'Study_Satisfaction',
        'Job Satisfaction': 'Job_Satisfaction',
        'Work/Study Hours': 'Work_Study_Hours',
        'Financial Stress': 'Financial_Stress'
    }
    
    df_clean = df.rename(columns=column_mapping)
    
    # Step 2: Remove rows with missing values (only 3, so it's safe)
    rows_before_missing = len(df_clean)
    df_clean = df_clean.dropna()
    rows_after_missing = len(df_clean)
    
    # Step 3: Remove cities with fewer than 20 students
    MIN_STUDENTS_PER_CITY = 20
    
    city_counts = df_clean['City'].value_counts()
    valid_cities = city_counts[city_counts >= MIN_STUDENTS_PER_CITY].index
    
    rows_before_city_filter = len(df_clean)
    df_clean = df_clean[df_clean['City'].isin(valid_cities)]
    rows_after_city_filter = len(df_clean)
    
    removed_city_count = len(city_counts) - len(valid_cities)
    rows_removed_by_city = rows_before_city_filter - rows_after_city_filter
    
    # Step 4: Ensure Depression is integer type
    df_clean['Depression'] = df_clean['Depression'].astype(int)
    
    # Step 5: Remove useless columns (constant values)
    columns_to_remove = []
    
    # Check for columns with only one unique value
    for col in df_clean.columns:
        if df_clean[col].nunique() == 1:
            columns_to_remove.append(col)
    
    if columns_to_remove:
        df_clean = df_clean.drop(columns=columns_to_remove)
    
    # Store cleaning stats
    cleaning_stats = {
        'rows_removed_missing': rows_before_missing - rows_after_missing,
        'rows_removed_city': rows_removed_by_city,
        'cities_removed': removed_city_count,
        'min_students_threshold': MIN_STUDENTS_PER_CITY
    }
    
    return df_clean, columns_to_remove, column_mapping, cleaning_stats


def get_column_info(df):
    """
    Get information about columns (useful for data quality reporting)
    
    Args:
        df: DataFrame
        
    Returns:
        dict: Information about constant columns
    """
    constant_cols = {}
    
    for col in df.columns:
        unique_count = df[col].nunique()
        if unique_count == 1:
            constant_cols[col] = df[col].iloc[0]
    
    return constant_cols


def get_city_stats(df, min_students=1):
    """
    Calculate depression statistics by city
    
    Args:
        df: Cleaned DataFrame
        min_students: Minimum number of students required (default: 1)
        
    Returns:
        pd.DataFrame: City-level statistics (filtered if min_students > 1)
    """
    city_stats = df.groupby('City').agg({
        'Depression': ['sum', 'count', 'mean'],
        'Academic_Pressure': 'mean',
        'Sleep_Duration': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
    }).reset_index()
    
    # Flatten column names
    city_stats.columns = ['City', 'Depression_Count', 'Total_Students', 
                          'Depression_Rate', 'Avg_Academic_Pressure', 'Most_Common_Sleep']
    
    # Convert rate to percentage
    city_stats['Depression_Rate'] = city_stats['Depression_Rate'] * 100
    
    # Filter cities with minimum number of students
    if min_students > 1:
        city_stats = city_stats[city_stats['Total_Students'] >= min_students]
    
    # Sort by depression rate
    city_stats = city_stats.sort_values('Depression_Rate', ascending=False)
    
    return city_stats


def get_demographic_stats(df):
    """
    Calculate depression statistics by demographics (Gender, Degree, etc.)
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        dict: Dictionary containing demographic statistics
    """
    stats = {}
    
    # Gender statistics
    if 'Gender' in df.columns:
        gender_stats = df.groupby('Gender').agg({
            'Depression': ['sum', 'count', 'mean']
        }).reset_index()
        gender_stats.columns = ['Gender', 'Depression_Count', 'Total', 'Depression_Rate']
        gender_stats['Depression_Rate'] = gender_stats['Depression_Rate'] * 100
        stats['gender'] = gender_stats
    
    # Degree statistics
    if 'Degree' in df.columns:
        degree_stats = df.groupby('Degree').agg({
            'Depression': ['sum', 'count', 'mean']
        }).reset_index()
        degree_stats.columns = ['Degree', 'Depression_Count', 'Total', 'Depression_Rate']
        degree_stats['Depression_Rate'] = degree_stats['Depression_Rate'] * 100
        stats['degree'] = degree_stats
    
    return stats


def get_sleep_stats(df):
    """
    Calculate depression statistics by sleep duration
    Excludes 'Others' category as it's not a clear sleep duration
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        pd.DataFrame: Sleep duration statistics
    """
    # Filter out 'Others' before aggregation
    df_sleep = df[df['Sleep_Duration'] != 'Others'].copy()
    
    sleep_stats = df_sleep.groupby('Sleep_Duration').agg({
        'Depression': ['sum', 'count', 'mean']
    }).reset_index()
    
    sleep_stats.columns = ['Sleep_Duration', 'Depression_Count', 'Total', 'Depression_Rate']
    sleep_stats['Depression_Rate'] = sleep_stats['Depression_Rate'] * 100
    
    # Order sleep categories logically
    sleep_order = ['Less than 5 hours', '5-6 hours', '7-8 hours', 'More than 8 hours']
    
    sleep_stats['Sleep_Duration'] = pd.Categorical(
        sleep_stats['Sleep_Duration'], 
        categories=sleep_order, 
        ordered=True
    )
    
    sleep_stats = sleep_stats.sort_values('Sleep_Duration')
    
    return sleep_stats