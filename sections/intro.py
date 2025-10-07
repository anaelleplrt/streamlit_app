import streamlit as st

def show():
    """
    Display introduction section with context and objectives
    """
    st.markdown("## 🧠 Introduction: Understanding Student Mental Health")
    
    # Hook - why this matters
    st.markdown("""
    ### Why This Matters
    
    Mental health among students has become a critical concern in educational institutions worldwide. 
    Depression, in particular, affects academic performance, social relationships, and overall well-being.
    
    Understanding the **patterns, risk factors, and demographics** associated with student depression 
    can help institutions develop targeted support systems and early intervention strategies.
    """)
    
    # Dataset context
    st.markdown("""
    ### About This Dataset
    
    This analysis uses a comprehensive dataset of **27,901 students** containing information about:
    - **Demographics**: Age, Gender, City, Education Level
    - **Academic factors**: Academic Pressure, CGPA, Study Hours, Study Satisfaction
    - **Lifestyle**: Sleep Duration, Dietary Habits
    - **Mental Health**: Depression Status, Suicidal Thoughts, Family History
    - **Financial**: Financial Stress
    
    **Source**: Kaggle - Student Depression Dataset (Anonymized)
    """)
    
    # Key questions
    st.markdown("""
    ### Key Questions We'll Answer
    
    1. **Geographic Patterns**: Which cities have the highest depression rates?
    2. **Demographic Factors**: How do gender and education level affect depression rates?
    3. **Risk Factors**: What factors are most strongly associated with depression?
    4. **Sleep & Health**: How does sleep duration relate to mental health?
    5. **Academic Pressure**: Is there a correlation between academic stress and depression?
    """)
    
    # Navigation guide
    st.info("""
    💡 **How to use this dashboard:**
    - Use the **sidebar filters** to explore specific subgroups
    - **Hover over charts** for detailed information
    - Each section provides **key insights** based on the data
    """)
    
    # Ethical disclaimer
    st.warning("""
    ⚠️ **Important Note:**
    
    This dashboard is designed for **educational and research purposes only**. 
    It should not be used for individual diagnosis or medical advice. 
    If you or someone you know is struggling with depression, please seek help from qualified mental health professionals.
    """)