"""
Overview section: KPIs and high-level trends
"""

import streamlit as st
import pandas as pd
from utils.viz import (create_income_inequality_chart, format_percentage, 
                       format_large_number)


def render(tables: dict, selected_disease: str, rate_type: str):
    """
    Render the overview section with KPIs
    
    Args:
        tables: Dictionary of prepared tables
        selected_disease: Currently selected disease
        rate_type: 'prevalence' or 'incidence'
    """
    
    st.markdown("## 📊 Overview: The Big Picture")
    st.markdown(f"**Disease:** {selected_disease} | **Metric:** {rate_type.capitalize()}")
    
    st.markdown("---")
    
    # KPI HEADER - Key metrics tied to filters
    st.markdown("### 🎯 Key Performance Indicators")
    
    if not tables['by_income'].empty:
        income_data = tables['by_income'][
            (tables['by_income']['varTauxLib'] == selected_disease) &
            (tables['by_income']['type'] == rate_type)
        ]
        
        if not income_data.empty and 'income_decile' in income_data.columns:
            # Calculate key metrics
            d1_data = income_data[income_data['income_decile'] == 1]
            d10_data = income_data[income_data['income_decile'] == 10]
            
            if not d1_data.empty and not d10_data.empty:
                d1_rate = d1_data['txStandDir'].values[0]
                d10_rate = d10_data['txStandDir'].values[0]
                d1_pop = d1_data['poids1'].sum() if 'poids1' in d1_data.columns else 0
                d10_pop = d10_data['poids1'].sum() if 'poids1' in d10_data.columns else 0
                
                ratio = d1_rate / d10_rate if d10_rate > 0 else 0
                difference = d1_rate - d10_rate
                mean_rate = income_data['txStandDir'].mean()
                
                # Display KPIs in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="Poorest 10% (D1)",
                        value=format_percentage(d1_rate),
                        delta=f"+{format_percentage(d1_rate - mean_rate)} vs avg",
                        delta_color="inverse",
                        help="Disease rate in the lowest income decile"
                    )
                    if d1_pop > 0:
                        st.caption(f"👥 ~{format_large_number(d1_pop)} people")
                
                with col2:
                    st.metric(
                        label="Richest 10% (D10)",
                        value=format_percentage(d10_rate),
                        delta=f"{format_percentage(d10_rate - mean_rate)} vs avg",
                        delta_color="normal",
                        help="Disease rate in the highest income decile"
                    )
                    if d10_pop > 0:
                        st.caption(f"👥 ~{format_large_number(d10_pop)} people")
                
                with col3:
                    st.metric(
                        label="Inequality Ratio",
                        value=f"{ratio:.2f}x",
                        delta=None,
                        help="How many times higher the rate is for poorest vs richest"
                    )
                    # Color-code severity
                    if ratio >= 2.5:
                        st.caption("🔴 High inequality")
                    elif ratio >= 1.5:
                        st.caption("🟡 Moderate inequality")
                    else:
                        st.caption("🟢 Low inequality")
                
                with col4:
                    st.metric(
                        label="Absolute Gap",
                        value=format_percentage(difference),
                        delta=None,
                        help="Percentage point difference between D1 and D10"
                    )
                    st.caption(f"📊 Mean: {format_percentage(mean_rate)}")
                
                # Insight box
                st.markdown("---")
                st.markdown(f"""
                <div style='background-color: #f0f9ff; border-left: 4px solid #2563eb; 
                            padding: 1rem; margin: 1rem 0;'>
                <strong>💡 Key Insight:</strong> For {selected_disease}, people in the <strong>poorest 
                income bracket have {ratio:.1f} times higher</strong> {rate_type} rates compared to 
                the richest. This translates to <strong>{format_percentage(difference)} more cases</strong> 
                per 100 people—a substantial and measurable health inequality.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Insufficient data for D1 or D10 calculation")
        else:
            st.warning("⚠️ No income decile data available for selected disease")
    else:
        st.error("❌ No data available. Please check data loading.")
    
    st.markdown("---")
    
    # HIGH-LEVEL TREND: Income Gradient
    st.markdown("### 📈 The Income Gradient")
    st.markdown("""
    The chart below shows how disease rates vary across all income levels. 
    **Notice the clear gradient:** rates typically decrease as income increases.
    
    - **Red bars** = Lower income (higher rates)
    - **Green bars** = Higher income (lower rates)
    - **Error bars** = 95% confidence intervals (statistical uncertainty)
    """)
    
    if not tables['by_income'].empty:
        fig = create_income_inequality_chart(
            tables['by_income'],
            selected_disease,
            rate_type
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional stats
        with st.expander("📊 Statistical Details"):
            income_data = tables['by_income'][
                (tables['by_income']['varTauxLib'] == selected_disease) &
                (tables['by_income']['type'] == rate_type)
            ]
            
            if not income_data.empty:
                st.markdown(f"""
                **Rate Statistics Across All Deciles:**
                - Minimum: {format_percentage(income_data['txStandDir'].min())} (typically D10)
                - Maximum: {format_percentage(income_data['txStandDir'].max())} (typically D1)
                - Mean: {format_percentage(income_data['txStandDir'].mean())}
                - Standard Deviation: {format_percentage(income_data['txStandDir'].std())}
                - Coefficient of Variation: {(income_data['txStandDir'].std() / income_data['txStandDir'].mean()):.2%}
                
                **Interpretation:** A higher coefficient of variation indicates greater inequality 
                across income groups.
                """)
    else:
        st.warning("⚠️ No income data available to display chart")
    
    st.markdown("---")
    
    # Population coverage summary
    st.markdown("### 👥 Population Coverage")
    
    if not tables['by_income'].empty:
        income_data = tables['by_income'][
            (tables['by_income']['varTauxLib'] == selected_disease) &
            (tables['by_income']['type'] == rate_type)
        ]
        
        if 'poids1' in income_data.columns:
            total_pop = income_data['poids1'].sum()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                This analysis covers approximately **{format_large_number(total_pop)} people** 
                across all income deciles in France.
                
                The data represents administrative health records from CNAM (National Health Insurance), 
                providing near-complete population coverage.
                """)
            
            with col2:
                st.info(f"""
                **Sample Size**
                
                Total: ~{format_large_number(total_pop)}
                
                Per decile: ~{format_large_number(total_pop/10)}
                
                This large sample ensures statistical robustness.
                """)