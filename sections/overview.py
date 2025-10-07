import streamlit as st
from utils.prep import get_city_stats, get_demographic_stats, get_sleep_stats
from utils.viz import create_city_map, create_demographic_chart, create_sleep_chart

def show(df):
    """
    Display overview section with KPIs and high-level visualizations
    
    Args:
        df: Cleaned DataFrame
    """
    st.markdown("## 📈 Overview: Key Statistics")
    
    # Calculate overall statistics
    total_students = len(df)
    depressed_students = df['Depression'].sum()
    depression_rate = (depressed_students / total_students) * 100
    
    avg_age = df['Age'].mean()
    avg_cgpa = df['CGPA'].mean()
    avg_academic_pressure = df['Academic_Pressure'].mean()
    
    # KPI Header
    st.markdown("### 🎯 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        "Total Students",
        f"{total_students:,}",
        help="Total number of students in the dataset after cleaning"
    )
    
    col2.metric(
        "Depression Rate",
        f"{depression_rate:.1f}%",
        help="Percentage of students reporting depression"
    )
    
    col3.metric(
        "Avg Academic Pressure",
        f"{avg_academic_pressure:.2f}/5",
        help="Average academic pressure score (scale 1-5)"
    )
    
    col4.metric(
        "Avg CGPA",
        f"{avg_cgpa:.2f}/10",
        help="Average Cumulative Grade Point Average"
    )
    
    st.markdown("---")
    
    # Depression distribution insight
    st.markdown("### 💡 Key Insight: Depression Prevalence")
    
    col_insight1, col_insight2 = st.columns([2, 1])
    
    with col_insight1:
        st.info(f"""
        **Depression is highly prevalent among students in this dataset.**
        
        - Out of **{total_students:,}** students, **{depressed_students:,}** ({depression_rate:.1f}%) report experiencing depression
        - This rate is significantly higher than general population estimates
        - The data suggests a critical need for mental health support in educational institutions
        """)
    
    with col_insight2:
        # Depression breakdown
        depression_breakdown = df['Depression'].value_counts()
        st.write("**Depression Status:**")
        st.write(f"✅ Not Depressed: {depression_breakdown.get(0, 0):,}")
        st.write(f"❌ Depressed: {depression_breakdown.get(1, 0):,}")
    
    st.markdown("---")
    
# Geographic distribution
    st.markdown("### 🗺️ Geographic Distribution")
    
    city_stats = get_city_stats(df, min_students=1)  # All remaining cities (already filtered in cleaning)
    
    total_cities = len(city_stats)
    
    st.info(f"""
    📊 Analyzing **{total_cities}** cities in the cleaned dataset.
    
    Cities with fewer than 20 students were removed during data cleaning to ensure statistical reliability.
    """)
    
    # Full width chart
    fig_city = create_city_map(city_stats)
    st.plotly_chart(fig_city, use_container_width=True)
    
    # Expandable table
    with st.expander(f"🔍 View all {total_cities} cities in analysis"):
        display_cities = city_stats[['City', 'Total_Students', 'Depression_Count', 'Depression_Rate']].copy()
        display_cities.columns = ['City', 'Total Students', 'Depressed Students', 'Depression Rate (%)']
        display_cities['Depression Rate (%)'] = display_cities['Depression Rate (%)'].round(1)
        
        st.dataframe(display_cities, use_container_width=True, hide_index=True)
    
    # Data quality note for cities
    with st.expander("🔍 View all cities and student counts"):
        all_cities = df['City'].value_counts().reset_index()
        all_cities.columns = ['City', 'Student_Count']
        all_cities['Depression_Rate'] = all_cities['City'].map(
            df.groupby('City')['Depression'].mean() * 100
        )
        all_cities = all_cities.sort_values('Student_Count', ascending=False)
        
        st.dataframe(all_cities, use_container_width=True, hide_index=True)
        
    # Demographics
    st.markdown("### 👥 Demographic Analysis")
    
    demo_stats = get_demographic_stats(df)
    
    col_demo1, col_demo2 = st.columns(2)
    
    with col_demo1:
        st.markdown("#### Gender Comparison")
        fig_gender = create_demographic_chart(demo_stats, 'gender')
        st.plotly_chart(fig_gender, use_container_width=True)
        
        # Gender insight
        gender_data = demo_stats['gender']
        if len(gender_data) > 0:
            highest_gender = gender_data.loc[gender_data['Depression_Rate'].idxmax()]
            st.caption(f"**{highest_gender['Gender']}** students show a little higher depression rates at {highest_gender['Depression_Rate']:.1f}%")
    
    with col_demo2:
        st.markdown("#### Education Level Comparison")
        fig_degree = create_demographic_chart(demo_stats, 'degree')
        st.plotly_chart(fig_degree, use_container_width=True)
        
        # Degree insight with explanation
        degree_data = demo_stats['degree']
        if len(degree_data) > 0:
            highest_degree = degree_data.loc[degree_data['Depression_Rate'].idxmax()]
            st.caption(f"**{highest_degree['Degree']}** students have the highest rate at {highest_degree['Depression_Rate']:.1f}%")
            
            # Add explanation note
            with st.expander("ℹ️ About education levels"):
                st.write("""
                **Education levels in this dataset:**
                
                - **Class 12**: High school students (12th grade, age ~17-18)
                - **Bachelor's degrees**: BA, BSc, BCA, B.Tech, B.Pharm, etc.
                - **Master's degrees**: M.Tech, MBA, MSc, MA, etc.
                - **Professional degrees**: BBA, BCA, etc.
                
                The dataset includes both high school and university students.
                """)
    
    st.markdown("---")
    
    # Sleep analysis
    st.markdown("### 😴 Sleep Duration & Depression")
    
    sleep_stats = get_sleep_stats(df)
    
    col_sleep1, col_sleep2 = st.columns([3, 1])
    
    with col_sleep1:
        fig_sleep = create_sleep_chart(sleep_stats)
        st.plotly_chart(fig_sleep, use_container_width=True)
    
    with col_sleep2:
        st.markdown("**Depression Rate by Sleep:**")
        for idx, row in sleep_stats.iterrows():
            st.write(f"**{row['Sleep_Duration']}**")
            st.write(f"→ {row['Depression_Rate']:.1f}%")
            st.write("")
    
    # Sleep insight
    st.warning("""
    **⚠️ Sleep Pattern Observation:**
    
    Students with less sleep tend to show different depression patterns. 
    The relationship between sleep duration and mental health appears to be significant and warrants further investigation.
    """)
    
    st.markdown("---")
    
    # Summary
    st.markdown("### 📊 Overview Summary")
    
    st.success("""
    **Key Takeaways from Overview:**
    
    1. **High Prevalence**: Depression affects a significant portion of the student population
    2. **Geographic Variation**: Depression rates vary considerably across different cities
    3. **Demographic Differences**: Gender and education level show distinct patterns
    4. **Sleep Connection**: Sleep duration appears to be associated with depression rates
    
    👉 **Next**: Explore the "Deep Dive" section for detailed correlation analysis and risk factors.
    """)