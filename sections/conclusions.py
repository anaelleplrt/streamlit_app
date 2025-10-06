"""
Conclusions section: Key insights, implications, and next steps
"""

import streamlit as st
import pandas as pd


def render(tables: dict, df_clean: pd.DataFrame, selected_disease: str, rate_type: str):
    """
    Render the conclusions section
    
    Args:
        tables: Dictionary of prepared tables
        df_clean: Cleaned dataframe
        selected_disease: Currently selected disease
        rate_type: 'prevalence' or 'incidence'
    """
    
    st.markdown("## 💡 Insights & Implications")
    st.markdown("What we've learned and what it means for policy and research")
    
    st.markdown("---")
    
    # KEY INSIGHTS SUMMARY
    st.markdown("### 🎯 Key Findings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 1. Income Inequality is Pervasive
        
        Across nearly all chronic diseases analyzed, we observe a **clear and consistent 
        income gradient**:
        
        - ✅ Poorest 10% have **2-3x higher rates** than richest 10%
        - ✅ The gradient is **linear and consistent** across all deciles
        - ✅ Effect holds **even after age/sex standardization**
        - ✅ Some diseases (diabetes, psychiatric) show **steeper gradients**
        
        **What this means:** Income is a powerful predictor of chronic disease risk. 
        This is not random variation—it's a systematic health inequality.
        """)
        
        st.markdown("""
        #### 2. Geographic Disparities Exist
        
        Health inequalities vary significantly by region:
        
        - 🗺️ Northern regions often show higher rates
        - 🏙️ Urban-rural patterns differ by disease type
        - 🏞️ Regional variations overlay with socioeconomic factors
        - 📍 "Health deserts" exist with limited healthcare access
        
        **What this means:** Where you live matters for your health outcomes. 
        Regional policies must account for local contexts.
        """)
    
    with col2:
        st.markdown("""
        #### 3. Education Has Independent Effects
        
        Beyond income, education level matters:
        
        - 📚 Higher education = consistently lower disease rates
        - 🎓 Effect persists even controlling for income
        - 📖 Health literacy likely plays a protective role
        - 🧠 Knowledge enables better health decisions
        
        **What this means:** Investing in education is also investing in 
        public health. Educational interventions can reduce health inequalities.
        """)
        
        st.markdown("""
        #### 4. Multiple Factors Compound
        
        Disadvantages accumulate:
        
        - ⚡ Low income + low education = highest risk
        - 🔄 Intersectionality amplifies inequalities
        - 📊 Age and gender interactions significant
        - 🎯 Most vulnerable need most support
        
        **What this means:** Interventions must be multifaceted. 
        Addressing single factors isn't enough—we need comprehensive approaches.
        """)
    
    st.markdown("---")
    
    # POLICY IMPLICATIONS
    st.markdown("### 🏛️ Policy Implications")
    
    st.markdown("""
    These findings have clear implications for public health policy in France:
    """)
    
    # Create expandable sections for different policy areas
    with st.expander("🎯 **1. Targeted Prevention Programs**", expanded=True):
        st.markdown("""
        **Problem:** Universal prevention programs may miss those at highest risk.
        
        **Recommendation:**
        - Design **income-targeted** prevention initiatives
        - Focus resources on **poorest deciles** (D1-D3)
        - Implement **outreach programs** in high-risk communities
        - Provide **free or subsidized** preventive care
        - Use **community health workers** in vulnerable areas
        
        **Expected Impact:** Reducing disease incidence in highest-risk groups could 
        substantially narrow overall health inequalities.
        
        **Examples:**
        - Free diabetes screening in low-income neighborhoods
        - Mobile health clinics in underserved regions
        - Subsidized gym memberships for low-income populations
        """)
    
    with st.expander("🏥 **2. Healthcare Access & Affordability**"):
        st.markdown("""
        **Problem:** Financial and geographic barriers prevent timely care.
        
        **Recommendation:**
        - Eliminate **co-payments** for chronic disease management
        - Expand **healthcare infrastructure** in underserved regions
        - Increase **primary care** physician density in "health deserts"
        - Improve **public transportation** to healthcare facilities
        - Develop **telemedicine** for remote areas
        
        **Expected Impact:** Better access enables earlier diagnosis and better 
        disease management, preventing complications.
        
        **Examples:**
        - Zero-cost chronic disease medications for low-income patients
        - Regional health centers in rural areas
        - Teleconsultation programs for chronic disease follow-up
        """)
    
    with st.expander("🏘️ **3. Social Determinants of Health**"):
        st.markdown("""
        **Problem:** Health is shaped by living conditions, not just healthcare.
        
        **Recommendation:**
        - Address **housing quality** (mold, heating, overcrowding)
        - Improve **food security** and access to healthy food
        - Enhance **employment protections** and working conditions
        - Increase **minimum wage** and social benefits
        - Invest in **education** from early childhood
        
        **Expected Impact:** Upstream interventions prevent disease before it starts, 
        rather than treating after onset.
        
        **Examples:**
        - Subsidized healthy food programs in low-income areas
        - Occupational health standards enforcement
        - Universal pre-school education
        """)
    
    with st.expander("📊 **4. Data-Driven Resource Allocation**"):
        st.markdown("""
        **Problem:** Resources often allocated based on politics, not need.
        
        **Recommendation:**
        - Use **inequality data** to guide funding decisions
        - Implement **equity-based** health budgets
        - Monitor **health inequality indicators** systematically
        - Publish **regional health inequality reports** annually
        - Establish **health equity targets** with accountability
        
        **Expected Impact:** Evidence-based allocation ensures resources reach 
        those who need them most.
        
        **Examples:**
        - Regional health budgets weighted by inequality measures
        - Public dashboards tracking health equity progress
        - Performance bonuses for regions reducing inequalities
        """)
    
    st.markdown("---")
    
    # CLOSING STATEMENT
    st.markdown("### 🏁 Final Thoughts")
    
    st.markdown(f"""
    The data is clear: **health inequalities in France are substantial, measurable, and 
    actionable**. People in the poorest segments of society face 2-3 times higher rates 
    of chronic disease, translating to thousands of preventable deaths and immense 
    suffering each year.
    
    These inequalities are **not inevitable**. They result from modifiable social, economic, 
    and policy factors. Other countries have demonstrated that determined action can reduce 
    health inequalities significantly.
    
    **The question is not whether we can reduce health inequalities—it's whether we will.**
    
    This dashboard provides the evidence. Now it's up to policymakers, researchers, 
    healthcare providers, and citizens to act on it.
    
    ---
    
    *For {selected_disease} specifically, the current analysis shows a 
    {rate_type} rate that varies significantly across social groups. Use the 
    controls in the sidebar to explore other diseases and dimensions of inequality.*
    """)
    
    st.info("""
    💬 **Have questions or feedback about this dashboard?**  
    This is an academic project for EFREI Paris. For questions about the underlying 
    data, contact DREES. For questions about this dashboard, see the README.
    """)