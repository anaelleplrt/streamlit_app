"""
The Inequality That Kills: Chronic Diseases & Social Inequalities Dashboard
EFREI Paris - Data Storytelling Project 2025

Main Streamlit application orchestrating all sections
Following recommended project structure
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add sections and utils to path
sys.path.append(str(Path(__file__).parent))

# Import utility functions
from utils.io import load_data, get_license_info
from utils.prep import clean_data, make_tables, get_data_quality_report

# Import section modules
from sections import intro, overview, deep_dives, conclusions


# ======================
# PAGE CONFIGURATION
# ======================
st.set_page_config(
    page_title="Data Storytelling | EFREI 2025",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'Data Storytelling Dashboard - EFREI Paris 2025'
    }
)


# ======================
# CUSTOM CSS STYLING
# ======================
st.markdown("""
<style>
    /* Main content styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 0.5rem;
    }
    
    /* Improve table readability */
    [data-testid="stDataFrame"] {
        font-size: 0.9rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ======================
# DATA LOADING
# ======================
@st.cache_data(show_spinner=False)
def load_and_prepare_data():
    """
    Load and prepare all data tables
    Returns: (raw_df, clean_df, tables_dict, quality_report)
    """
    # Load from local CSV
    df_raw = load_data()
    
    if df_raw.empty:
        return df_raw, df_raw, {}, {}
    
    # Clean and prepare
    df_clean = clean_data(df_raw)
    
    # Create analysis tables
    tables = make_tables(df_clean)
    
    # Quality report
    quality_report = get_data_quality_report(df_clean)
    
    return df_raw, df_clean, tables, quality_report


# ======================
# MAIN APPLICATION
# ======================
def main():
    """Main application logic"""
    
    # Load data
    with st.spinner("Loading data from local CSV..."):
        df_raw, df_clean, tables, quality_report = load_and_prepare_data()
    
    # Check if data loaded successfully
    if df_clean.empty:
        st.error("""
         **Failed to load data**
        
        Please ensure `er_inegalites_maladies_chroniques.csv` is in the `data/` folder.
        
        Download it from: https://data.drees.solidarites-sante.gouv.fr/
        """)
        st.stop()
    
    # ======================
    # SIDEBAR CONTROLS
    # ======================
    with st.sidebar:        
        st.markdown("# Dashboard Controls")
        st.markdown("---")
        
        # Get available diseases (CORRECT camelCase)
        all_diseases = sorted(df_clean['varTauxLib'].unique().tolist())
        
        if not all_diseases:
            st.error("No diseases found in dataset")
            st.stop()

        # NAVIGATION: Section selector
        st.markdown("### Navigation")
        
        section = st.radio(
            "Jump to section:",
            options=[
                "Introduction",
                "Overview", 
                "Data Quality",
                "Deep Dives",
                "Conclusions"
            ],
            label_visibility="collapsed"
        )
        
        # FILTER 1: Disease selection
        selected_disease = st.selectbox(
            "**Select Disease**",
            options=all_diseases,
            index=0,
            help="Choose a chronic disease to analyze throughout the dashboard"
        )
        
        # FILTER 2: Rate type (prevalence vs incidence)
        rate_type = st.radio(
            "**Rate Type**",
            options=['prevalence', 'incidence'],
            help="""
            - **Prevalence**: Existing cases (how many people currently have it)
            - **Incidence**: New cases (how many people newly developed it)
            """
        )
        
        # FILTER 3: Comparison dimension
        comparison_mode = st.selectbox(
            "**Compare By**",
            options=[
                'Income Decile',
                'Region', 
                'Education',
                'Socio-Professional Group'
            ],
            help="Choose which demographic dimension to analyze in detail"
        )
        st.markdown("---")
        # DATA INFO
        st.markdown("### Dataset Info")
        st.caption(f"**Records:** {quality_report.get('total_records', 0):,}")
        st.caption(f"**Diseases:** {len(all_diseases)}")
        st.caption(f"**Memory:** {quality_report.get('memory_usage', 0):.1f} MB")
        st.markdown("---")
        
    
    # ======================
    # MAIN CONTENT AREA
    # ======================
    
    # Route to appropriate section based on navigation
    if "Introduction" in section:
        intro.render()
    
    elif "Overview" in section:
        overview.render(tables, selected_disease, rate_type)
    
    elif "Data Quality" in section:
        render_data_quality_section(df_clean, quality_report)
        
    elif "Deep Dives" in section:
        deep_dives.render(tables, df_clean, selected_disease, rate_type, comparison_mode)
    
    elif "Conclusions" in section:
        conclusions.render(tables, df_clean, selected_disease, rate_type)
    
    
    
    # ======================
    # FOOTER
    # ======================
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 1rem 0;'>
        <strong>Data Storytelling Dashboard<br>
        EFREI Paris - 2025 | Student: Anaëlle Pollart<br>
        Source: DREES ER 1243 | Teacher : Mano Mathew
    </div>
    """, unsafe_allow_html=True)


def render_data_quality_section(df_clean: pd.DataFrame, quality_report: dict):
    """
    Render data quality and validation section
    
    Args:
        df_clean: Cleaned dataframe
        quality_report: Quality metrics dictionary
    """
    st.markdown("## Data Quality")
    st.markdown("Comprehensive data quality checks")
    
    st.markdown("---")
    
    # QUALITY METRICS
    st.markdown("### Quality Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Records",
            f"{quality_report.get('total_records', 0):,}",
            help="Total number of data records loaded"
        )
    
    with col2:
        st.metric(
            "Total Columns",
            quality_report.get('total_columns', 0),
            help="Number of variables in dataset"
        )
    
    with col3:
        duplicates = quality_report.get('duplicate_rows', 0)
        st.metric(
            "Duplicate Rows",
            duplicates,
            help="Number of exact duplicate records"
        )
    
    with col4:
        st.metric(
            "Memory Usage",
            f"{quality_report.get('memory_usage', 0):.1f} MB",
            help="Dataset memory footprint"
        )

    # DATA SAMPLE
    st.markdown("---")
    st.markdown("### Data Sample")
    st.markdown("First 10 rows of the dataset:")
    
    st.dataframe(df_clean.head(10), use_container_width=True)

    # COLUMN DESCRIPTIONS
    st.markdown("---")
    st.markdown("### Column Descriptions")
    
    st.markdown("""
        **Key Columns:**
        
        - `varTauxLib`: Disease name (e.g., "Diabète", "Maladies cardiovasculaires")
        - `type`: Rate type - "prevalence" or "incidence"
        - `varGroupage`: Grouping variable (SEXE, classeAge10, FISC_REG_S, etc.)
        - `valGroupage`: Value of grouping variable (e.g., "1" for male, "44" for region)
        - `varPartition`: Partition variable (optional sub-grouping)
        - `valPartition`: Value of partition variable
        
        **Rate Columns:**
        
        - `txNonStand`: Non-standardized rate (%)
        - `txStandDir`: Directly standardized rate (%)
        - `txStandIndir`: Indirectly standardized rate (%)
        - `*BB`: Lower bound of 95% confidence interval
        - `*BH`: Upper bound of 95% confidence interval
        
        **Weight Columns:**
        
        - `poids1`: Weighted population count for group
        - `poidsTot`: Total weighted population
        
        **Grouping Variables:**
        
        - `SEXE`: Gender (1=Male, 2=Female)
        - `classeAge10`: Age group in 10-year intervals
        - `FISC_REG_S`: Region code
        - `FISC_NIVVIEM_E2015_S_moy_10`: Income decile (1=poorest, 10=richest)
        - `EAR_GS_S`: Socio-professional group
        - `EAR_DIPLR_S`: Education level
        """)
    
    
    # MISSING DATA ANALYSIS
    st.markdown("---")
    st.markdown("### Missing Data Analysis")
    
    missing_by_col = quality_report.get('missing_by_column', {})
    
    if missing_by_col:
        # Filter columns with missing data
        missing_data = {k: v for k, v in missing_by_col.items() if v >= 0}
        
        if missing_data:
            missing_df = pd.DataFrame([
                {
                    'Column': col,
                    'Missing Count': count,
                    'Missing %': f"{(count / quality_report['total_records'] * 100):.2f}%"
                }
                for col, count in missing_data.items()
            ]).sort_values('Missing Count', ascending=False)
            
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("No missing data detected in any columns!")
    else:
        st.info("No missing data information available")
    

    # DATA CLEANING PROCESS
    st.markdown("---")
    st.markdown("### Data Cleaning & Processing")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Cleaning Steps Applied")
        st.markdown("""
        **1. Missing Values:**
        - Rows with missing `varTauxLib` or `type` → **Dropped**
        - Missing `valGroupage` or `varGroupage` → **Filtered during grouping**
        - Missing numeric values → **Converted to NaN** (not dropped)
        
        **2. Data Type Conversion:**
        - Numeric columns (`txStandDir`, `poids1`, etc.) → **Converted to float**
        - String columns (`varTauxLib`, `type`, etc.) → **Converted to string**
        - Invalid numeric values → **Set to NaN**
        
        **3. Filtering:**
        - `valGroupage == 'nan'` → **Excluded** from analysis
        - Empty string values → **Treated as missing**
        """)

    with col2:
        st.markdown("#### Impact on Dataset")
        
        original_rows = quality_report['total_records']
        
        # Calculate how many rows have critical missing values
        critical_missing = 0
        if 'varTauxLib' in df_clean.columns:
            critical_missing += df_clean['varTauxLib'].isna().sum()
        if 'type' in df_clean.columns:
            critical_missing += df_clean['type'].isna().sum()
        
        st.metric(
            "Rows After Cleaning",
            f"{original_rows:,}",
            help="Rows remaining after cleaning"
        )
        
        if critical_missing > 0:
            st.metric(
                "Rows Dropped",
                f"{critical_missing:,}",
                delta=f"-{(critical_missing/original_rows*100):.1f}%",
                delta_color="inverse"
            )
        else:
            st.success("No rows dropped due to missing critical data")
        
        # Show numeric conversion success
        numeric_cols = ['txStandDir', 'poids1', 'txNonStand']
        valid_numerics = sum([
            pd.api.types.is_numeric_dtype(df_clean[col]) 
            for col in numeric_cols if col in df_clean.columns
        ])
        
        st.metric(
            "Numeric Columns Valid",
            f"{valid_numerics}/{len([c for c in numeric_cols if c in df_clean.columns])}",
            help="Successfully converted numeric columns"
        )
    
    
    # REPRODUCIBILITY
    st.markdown("---")
    st.markdown("### Reproducibility Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Environment
        
        **Python Version:** 3.8+  
        **Streamlit Version:** ≥1.33.0  
        **Key Dependencies:**
        - pandas 
        - plotly 
        - numpy 
        
        All dependencies specified in `requirements.txt`
        """)
    
    with col2:
        st.markdown("""
        #### Data Source
        
        **Provider:** DREES (French Ministry of Health)  
        **Dataset:** ER 1243  
        **Format:** CSV  
        **Size:** 46,176 records and 20 columns
        
        Download from: [DREES Data Portal](https://data.drees.solidarites-sante.gouv.fr/)
        """)
    
    # CACHE STATUS
    st.markdown("---")
    st.markdown("### Performance & Caching")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Cache Status",
            "Active",
        )
    
    with col2:
        st.metric(
            "Load Time",
            "< 2s",
            help="Time to load and process data"
        )
    
    with col3:
        if st.button("Clear Cache & Reload"):
            st.cache_data.clear()
            st.rerun()
    


# ======================
# RUN APPLICATION
# ======================
if __name__ == "__main__":
    main()