"""
Deep dives section: Comparisons, distributions, and drilldowns
"""

import streamlit as st
import pandas as pd
from utils.viz import (create_comparison_chart, create_multiple_diseases_chart,
                       create_heatmap, create_inequality_ratio_chart)
from utils.prep import calculate_inequality_ratio, get_top_diseases


def render(tables: dict, df_clean: pd.DataFrame, selected_disease: str, 
           rate_type: str, comparison_mode: str):
    """
    Render the deep dives section with detailed analysis
    
    Args:
        tables: Dictionary of prepared tables
        df_clean: Cleaned dataframe
        selected_disease: Currently selected disease
        rate_type: 'prevalence' or 'incidence'
        comparison_mode: Selected comparison dimension
    """
    
    st.markdown("## 🔍 Deep Dives: Detailed Analysis")
    st.markdown("Explore health inequalities across multiple dimensions")
    
    st.markdown("---")
    
    # TAB STRUCTURE for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Comparative Analysis",
        "🔥 Inequality Heatmap", 
        "🏆 Disease Rankings",
        "🔬 Multi-Disease Comparison"
    ])
    
    # TAB 1: Comparative Analysis by Selected Dimension
    with tab1:
        st.markdown(f"### Comparison by {comparison_mode}")
        st.markdown(f"How does **{selected_disease}** vary across different {comparison_mode.lower()} groups?")
        
        # Map comparison mode to table
        table_map = {
            'Income Decile': ('by_income', 'income_decile'),
            'Region': ('by_region', 'region_code'),
            'Education': ('by_education', 'education_level'),
            'Socio-Professional Group': ('by_csp', 'csp_group')
        }
        
        table_name, col_name = table_map.get(comparison_mode, ('by_income', 'income_decile'))
        
        if tables[table_name].empty:
            st.warning(f"⚠️ No {comparison_mode} data available for this disease")
        else:
            # Filter controls
            col1, col2 = st.columns([3, 1])
            
            with col2:
                top_n = st.slider(
                    "Show top N groups",
                    min_value=5,
                    max_value=min(20, len(tables[table_name])),
                    value=10,
                    help="Limit display to top N groups by rate"
                )
            
            with col1:
                fig = create_comparison_chart(
                    tables[table_name],
                    selected_disease,
                    col_name,
                    rate_type,
                    top_n=top_n
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            with st.expander("📋 View Data Table"):
                display_data = tables[table_name][
                    (tables[table_name]['varTauxLib'] == selected_disease) &
                    (tables[table_name]['type'] == rate_type)
                ].copy()
                
                if not display_data.empty:
                    display_data = display_data.sort_values('txStandDir', ascending=False)
                    display_data = display_data.head(top_n)
                    
                    # Format for display
                    display_cols = [col_name, 'txStandDir', 'txStandDirModBB', 'txStandDirModBH']
                    display_cols = [c for c in display_cols if c in display_data.columns]
                    
                    st.dataframe(
                        display_data[display_cols].style.format({
                            'txStandDir': '{:.2f}%',
                            'txStandDirModBB': '{:.2f}%',
                            'txStandDirModBH': '{:.2f}%'
                        }),
                        use_container_width=True
                    )
    
    # TAB 2: Heatmap showing patterns across diseases and income
    with tab2:
        st.markdown("### The Inequality Heatmap")
        st.markdown("""
        This heatmap reveals patterns across multiple diseases and income levels.
        **Darker colors** indicate higher disease rates.
        """)
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            n_diseases = st.slider(
                "Number of diseases",
                min_value=5,
                max_value=15,
                value=10,
                help="Select how many diseases to display in heatmap"
            )
            
            sort_by = st.radio(
                "Sort by",
                options=['Rate', 'Inequality', 'Alphabetical'],
                help="How to order diseases"
            )
        
        with col1:
            if not tables['by_income'].empty:
                # Get top diseases
                if sort_by == 'Rate':
                    top_for_heatmap = get_top_diseases(df_clean, n=n_diseases, by=rate_type)
                elif sort_by == 'Inequality':
                    # Calculate inequality ratios and sort
                    ratios_list = []
                    all_diseases = df_clean['varTauxLib'].unique()
                    for disease in all_diseases:
                        ratio = calculate_inequality_ratio(tables['by_income'], disease, rate_type)
                        if not pd.isna(ratio) and ratio > 0:
                            ratios_list.append({'disease': disease, 'ratio': ratio})
                    
                    if ratios_list:
                        ratios_df = pd.DataFrame(ratios_list).nlargest(n_diseases, 'ratio')
                        top_for_heatmap = ratios_df['disease'].tolist()
                    else:
                        top_for_heatmap = get_top_diseases(df_clean, n=n_diseases, by=rate_type)
                else:  # Alphabetical
                    all_diseases = sorted(df_clean['varTauxLib'].unique())
                    top_for_heatmap = all_diseases[:n_diseases]
                
                if top_for_heatmap:
                    fig = create_heatmap(tables['by_income'], top_for_heatmap, rate_type)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No diseases available for heatmap")
            else:
                st.warning("⚠️ No income data available for heatmap")
        
        # Interpretation guide
        with st.expander("📖 How to Read This Heatmap"):
            st.markdown("""
            **What you're seeing:**
            - Each **row** is a disease
            - Each **column** is an income decile (D1=poorest, D10=richest)
            - **Color intensity** shows the disease rate (darker = higher)
            
            **What to look for:**
            - **Gradient patterns:** Do rates decrease from left (poor) to right (rich)?
            - **Hotspots:** Which diseases and income levels show highest rates?
            - **Outliers:** Any unexpected patterns?
            
            **Common patterns:**
            - Most chronic diseases show left-heavy patterns (higher in poorer deciles)
            - Some diseases show steeper gradients than others
            - The poorest decile (D1) typically shows the darkest colors
            """)
    
    # TAB 3: Inequality Rankings
    with tab3:
        st.markdown("### 🏆 Disease Inequality Rankings")
        st.markdown("Which diseases show the **strongest social gradient**?")
        
        if not tables['by_income'].empty:
            # Calculate inequality ratios for all diseases
            all_diseases = df_clean['varTauxLib'].unique()
            
            with st.spinner("Calculating inequality ratios..."):
                ratios_list = []
                for disease in all_diseases:
                    ratio = calculate_inequality_ratio(tables['by_income'], disease, rate_type)
                    if not pd.isna(ratio) and ratio > 0:
                        ratios_list.append({
                            'disease': disease,
                            'ratio': ratio
                        })
            
            if ratios_list:
                ratios_df = pd.DataFrame(ratios_list)
                
                # Controls
                col1, col2 = st.columns([3, 1])
                
                with col2:
                    show_top = st.slider(
                        "Show top N",
                        min_value=5,
                        max_value=min(15, len(ratios_df)),
                        value=10,
                        help="Number of diseases to display"
                    )
                
                with col1:
                    top_ratios = ratios_df.nlargest(show_top, 'ratio')
                    fig = create_inequality_ratio_chart(top_ratios)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Highest Inequality",
                        f"{ratios_df['ratio'].max():.2f}x",
                        help="Disease with strongest D1/D10 ratio"
                    )
                    st.caption(f"Disease: {ratios_df.loc[ratios_df['ratio'].idxmax(), 'disease']}")
                
                with col2:
                    st.metric(
                        "Average Inequality",
                        f"{ratios_df['ratio'].mean():.2f}x",
                        help="Mean inequality ratio across all diseases"
                    )
                
                with col3:
                    st.metric(
                        "Lowest Inequality",
                        f"{ratios_df['ratio'].min():.2f}x",
                        help="Disease with weakest D1/D10 ratio"
                    )
                    st.caption(f"Disease: {ratios_df.loc[ratios_df['ratio'].idxmin(), 'disease']}")
                
                # Interpretation
                st.info("""
                **💡 Interpretation:** An inequality ratio of 2.0x means the poorest 10% have 
                twice the disease rate of the richest 10%. Higher ratios indicate stronger 
                social gradients in health.
                """)
            else:
                st.warning("⚠️ Could not calculate inequality ratios")
        else:
            st.warning("⚠️ No income data available for rankings")
    
    # TAB 4: Multi-Disease Comparison
    with tab4:
        st.markdown("### 🔬 Compare Multiple Diseases")
        st.markdown("See how different chronic conditions compare across income levels")
        
        # Get available diseases (lowercase)
        all_diseases = sorted(df_clean['varTauxLib'].unique().tolist())
        
        # Disease multi-select
        col1, col2 = st.columns([3, 1])
        
        with col2:
            comparison_diseases = st.multiselect(
                "Select diseases to compare",
                options=all_diseases,
                default=all_diseases[:3] if len(all_diseases) >= 3 else all_diseases,
                max_selections=5,
                help="Choose up to 5 diseases to compare (max for readability)"
            )
        
        with col1:
            if comparison_diseases and not tables['by_income'].empty:
                fig = create_multiple_diseases_chart(
                    tables['by_income'],
                    comparison_diseases,
                    'income_decile',
                    rate_type
                )
                st.plotly_chart(fig, use_container_width=True)
            elif not comparison_diseases:
                st.info("👆 Select diseases above to compare them")
            else:
                st.warning("⚠️ No data available for comparison")
        
        # Side-by-side comparison table
        if comparison_diseases and not tables['by_income'].empty:
            with st.expander("📊 Side-by-Side Comparison Table"):
                comparison_data = []
                
                for disease in comparison_diseases:
                    disease_data = tables['by_income'][
                        (tables['by_income']['varTauxLib'] == disease) &
                        (tables['by_income']['type'] == rate_type)
                    ]
                    
                    if not disease_data.empty and 'income_decile' in disease_data.columns:
                        d1 = disease_data[disease_data['income_decile'] == 1]['txstanddir'].values
                        d10 = disease_data[disease_data['income_decile'] == 10]['txstanddir'].values
                        mean_rate = disease_data['txstanddir'].mean()
                        
                        if len(d1) > 0 and len(d10) > 0:
                            ratio = d1[0] / d10[0] if d10[0] > 0 else 0
                            
                            comparison_data.append({
                                'Disease': disease,
                                'D1 (Poorest)': f"{d1[0]:.2f}%",
                                'D10 (Richest)': f"{d10[0]:.2f}%",
                                'Gap': f"{d1[0] - d10[0]:.2f}%",
                                'Ratio': f"{ratio:.2f}x",
                                'Average': f"{mean_rate:.2f}%"
                            })
                
                if comparison_data:
                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, use_container_width=True)
                else:
                    st.warning("⚠️ No comparison data available")
    
    st.markdown("---")
    
    # SMALL MULTIPLES: Regional breakdown if data exists
    if not tables['by_region'].empty:
        with st.expander("🗺️ Regional Breakdown (Small Multiples)"):
            st.markdown(f"### Regional Variations: {selected_disease}")
            st.markdown("How does this disease vary across French regions?")
            
            region_data = tables['by_region'][
                (tables['by_region']['varTauxLib'] == selected_disease) &
                (tables['by_region']['type'] == rate_type)
            ]
            
            if not region_data.empty:
                region_data = region_data.sort_values('txStandDir', ascending=False)
                
                fig = create_comparison_chart(
                    tables['by_region'],
                    selected_disease,
                    'region_code',
                    rate_type,
                    top_n=13
                )
                st.plotly_chart(fig, use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Highest Rate Region",
                        f"{region_data['txStandDir'].max():.2f}%",
                        help="Region with highest disease rate"
                    )
                    st.caption(f"Code: {region_data.iloc[0]['region_code']}")
                
                with col2:
                    st.metric(
                        "Lowest Rate Region",
                        f"{region_data['txStandDir'].min():.2f}%",
                        help="Region with lowest disease rate"
                    )
                    st.caption(f"Code: {region_data.iloc[-1]['region_code']}")
                
                with col3:
                    regional_cv = (region_data['txStandDir'].std() / region_data['txStandDir'].mean())
                    st.metric("Regional Variation", f"{regional_cv:.1%}", help="Coefficient of variation")
            else:
                st.info("No regional data available")
    
    # Educational gradient
    if not tables['by_education'].empty:
        with st.expander("🎓 Educational Gradient"):
            st.markdown(f"### Education Level Impact: {selected_disease}")
            
            edu_data = tables['by_education'][
                (tables['by_education']['varTauxLib'] == selected_disease) &
                (tables['by_education']['type'] == rate_type)
            ]
            
            if not edu_data.empty:
                fig = create_comparison_chart(tables['by_education'], selected_disease, 'education_level', rate_type, top_n=10)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No education data available")
    
    # CSP
    if not tables['by_csp'].empty:
        with st.expander("👔 Occupational Categories"):
            st.markdown(f"### Socio-Professional Groups: {selected_disease}")
            
            csp_data = tables['by_csp'][
                (tables['by_csp']['varTauxLib'] == selected_disease) &
                (tables['by_csp']['type'] == rate_type)
            ]
            
            if not csp_data.empty:
                fig = create_comparison_chart(tables['by_csp'], selected_disease, 'csp_group', rate_type, top_n=12)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No occupational data available")