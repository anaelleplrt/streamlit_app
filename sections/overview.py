# sections/overview.py
import streamlit as st
import pandas as pd
import plotly.express as px

def render(df, tables, filters):
    st.header("Overview — Key Insights at a Glance")

    # -------------------------------
    # HEADLINE INSIGHT
    # -------------------------------
    if not df.empty:
        st.markdown(
            f"""
            ### Headline insight  
            Clothing deprivation varies greatly across Europe — in the selected filters,
            the **lowest** country is around **{df['obs_value'].min():.1f}%** and the **highest** about **{df['obs_value'].max():.1f}%**.
            """
        )
    else:
        st.warning("No data matches the current filters.")

    # -------------------------------
    # KPI METRICS
    # -------------------------------
    if not df.empty:
        kpi_mean = df["obs_value"].mean()
        kpi_min = df["obs_value"].min()
        kpi_max = df["obs_value"].max()
        num_countries = df["geo"].nunique()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Average deprivation (%)", f"{kpi_mean:.1f}")
        c2.metric("Minimum (%)", f"{kpi_min:.1f}")
        c3.metric("Maximum (%)", f"{kpi_max:.1f}")
        c4.metric("Countries included", num_countries)

    # -------------------------------
    # 1. TIME SERIES
    # -------------------------------
    if "year" in df.columns and "geo" in df.columns:
        st.subheader("Trend over time")
        fig = px.line(
            df,
            x="year",
            y="obs_value",
            color="geo",
            markers=True,
            labels={"obs_value": "% deprived", "year": "Year", "geo": "Country"},
            title="Clothing deprivation over time"
        )
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 2. MAP — STATIC CHOROPLETH
    # -------------------------------
    st.subheader("Map — selected year")
    map_data = df[df["year"] == filters.get("year_for_map")]
    if not map_data.empty:
        fig_map = px.choropleth(
            map_data,
            locations="iso3",
            color="obs_value",
            color_continuous_scale="Reds",
            hover_name="geo",
            labels={"obs_value": "% deprived"},
            title=f"Clothing deprivation in {filters.get('year_for_map')}"
        )
        fig_map.update_geos(showcountries=True, showcoastlines=True)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No data available for the selected year.")

    # -------------------------------
    # 3. RANKING BAR CHART
    # -------------------------------
    st.subheader("Country ranking")
    if not map_data.empty:
        rank_sorted = map_data.sort_values("obs_value", ascending=False)
        fig_rank = px.bar(
            rank_sorted,
            x="obs_value",
            y="geo",
            orientation="h",
            labels={"obs_value": "% deprived", "geo": "Country"},
            title=f"Ranking — Clothing deprivation ({filters.get('year_for_map')})"
        )
        fig_rank.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_rank, use_container_width=True)

    # -------------------------------
    # 4. DISTRIBUTION HISTOGRAM
    # -------------------------------
    if not map_data.empty:
        st.subheader("Distribution of deprivation (%)")
        fig_hist = px.histogram(
            map_data,
            x="obs_value",
            nbins=15,
            labels={"obs_value": "% deprived"},
            title=f"Distribution of clothing deprivation rates ({filters.get('year_for_map')})"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # -------------------------------
    # 6. ANIMATED MAP OVER TIME
    # -------------------------------
    if "iso3" in df.columns and "year" in df.columns:
        st.subheader("Animated map — evolution over time")
        fig_anim = px.choropleth(
            df,
            locations="iso3",
            color="obs_value",
            color_continuous_scale="Reds",
            hover_name="geo",
            animation_frame="year",
            labels={"obs_value": "% deprived"},
            title="Clothing deprivation evolution (animated)"
        )
        st.plotly_chart(fig_anim, use_container_width=True)

    # -------------------------------
    # DATA QUALITY
    # -------------------------------
    st.subheader("Data quality & validation")
    st.markdown(
        f"""
        - **Total rows:** {len(df)}  
        - **Duplicate rows:** {df.duplicated().sum()}  
        """
    )
    missing = df.isna().mean().sort_values(ascending=False)
    st.dataframe(missing.to_frame("Missing ratio").style.format("{:.1%}"))
    st.caption(
        "Source: Eurostat EU-SILC. Missingness computed after filtering. "
        "`OBS_FLAG` and `CONF_STATUS` are empty in this dataset."
    )

    # -------------------------------
    # DOWNLOAD BUTTON
    # -------------------------------
    st.subheader("Download filtered data")
    st.download_button(
        "Download CSV (filtered)",
        df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
