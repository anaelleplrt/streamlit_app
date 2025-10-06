"""
Introduction section: Context, objectives, and data caveats
"""

import streamlit as st
from utils.io import get_license_info


def render():
    """Render the introduction section"""
    
    # Main title and hook
    st.markdown("# *How Social Inequalities Shape Chronic Disease in France ?*")
    
    st.markdown("---")
    
    # Hook - Why this matters
    st.markdown("## Why This Matters ?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Health is not equally distributed in France.** People living in poverty face 
        dramatically higher rates of chronic diseases : diabetes, heart disease, psychiatric 
        disorders, and more,compared to wealthier citizens.
        
        This dashboard explores the **social determinants of health inequality** using 
        official data from the French Ministry of Health. We examine how income, education, 
        occupation, and geography shape who gets sick and who stays healthy.
        
        **The central question:** *Why do poor people die younger from chronic diseases?*
        """)
    
    with col2:
        st.info("""
        **Key Statistic**
        
        People in the poorest 10% of the population have **2-3 times higher** chronic disease 
        rates compared to the richest 10%.
        
        This translates to thousands of preventable deaths each year.
        """)
    
    st.markdown("---")
    
    # Context - What you'll discover
    st.markdown("## What You'll Discover ?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Patterns**
        - Income gradients in disease
        - Geographic disparities
        - Education effects
        - Intersectional impacts
        """)
    
    with col2:
        st.markdown("""
        **Analysis**
        - Standardized rates
        - Confidence intervals
        - Inequality ratios
        - Statistical validation
        """)
    
    with col3:
        st.markdown("""
        **Insights**
        - Policy implications
        - Vulnerable populations
        - Intervention priorities
        - Research gaps
        """)
    
    st.markdown("---")
    
    # Data source and methodology
    with st.expander("Data Source & Methodology", expanded=False):
        st.markdown("""
        ### Data Source
        
        This dashboard uses data from **DREES (Direction de la Recherche, des Études, 
        de l'Évaluation et des Statistiques)**, the research and statistics department 
        of the French Ministry of Health.
        
        **Dataset:** ER 1243 - "Social Inequalities and Chronic Diseases"  
        **Publication:** "Chronic diseases affect modest people more often and reduce their life expectancy further"  
        **Year:** Based on 2015-2017 cohort data  
        **License:** Open License / Licence Ouverte (Etalab)
        
        ### Methodology
        
        **Standardization:** All rates are standardized by age and sex using direct and 
        indirect methods. This allows fair comparisons between groups with different 
        demographic structures.
        
        **Confidence Intervals:** 95% confidence intervals are provided for all rates, 
        reflecting statistical uncertainty.
        
        **Data Source:** Administrative health data from CNAM (French National Health Insurance), 
        covering the entire population.
        
        ### Dimensions Analyzed
        
        - **Income:** Deciles (D1=poorest 10%, D10=richest 10%)
        - **Geography:** French metropolitan regions
        - **Education:** Diploma levels
        - **Occupation:** Socio-professional categories
        - **Demographics:** Age groups and gender
        
        ### Diseases Tracked
        
        The dataset covers chronic diseases from the CNAM disease mapping:
        - Cardiovascular diseases
        - Diabetes
        - Psychiatric disorders
        - Respiratory diseases
        - Cancers (categories only, subtypes excluded)
        - Neurological disorders
        - And more...
        """)
        
        st.markdown(get_license_info())
    
    
    st.markdown("---")
    
    # Navigation guide
    st.markdown("## Dashboard Guide")
    
    st.markdown("""
    This dashboard is organized into four main sections:
    
    1. **Overview** - High-level KPIs and trends
    2. **Data Quality** - Validation and methodology details
    3. **Deep Dives** - Detailed comparisons and distributions
    4. **Conclusions** - Key insights and implications
    
    Use the **sidebar controls** to filter by disease, rate type, and demographic dimensions.
    All charts are **interactive**—hover for details, click legends to filter.
    """)
    
    st.success("""
    **Ready to explore?** Use the sidebar to select a disease and start discovering 
    patterns of health inequality in France.
    """)