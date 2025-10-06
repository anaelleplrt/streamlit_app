# sections/intro.py
import streamlit as st
import pandas as pd

def render(df, tables, filters):
    st.header("Introduction & Context")

    st.subheader("Why this topic?")
    st.markdown(
        """
        The ability to **replace worn-out clothes with new ones** (excluding second-hand)
        is a tangible indicator of **living standards**.  
        The inability to do so reflects **material deprivation**, monitored by Eurostat
        through the European social statistics survey (EU-SILC).  
        This dashboard aims to make **differences between countries** and between
        **socio-economic groups** (gender, age, income) visible and to track their **evolution over time**.
        """
    )

    st.subheader("Problem statement & objectives")
    st.markdown(
        """
        - **Main question:** Who in Europe **cannot afford** to buy new clothes?  
          How does this vary **over time**, **across countries**, and **between socio-economic groups**?
        - **Objectives:**
          1) Visualize the **multi-year trend**;
          2) **Compare** countries (map + ranking);
          3) Highlight differences by **gender**, **age**, and **income**;
          4) Provide **actionable insights** for policy makers, NGOs, and the media.
        """
    )

    st.subheader("Data source")
    st.markdown(
        """
        - **Eurostat** — *Persons who cannot afford to replace worn-out clothes by some new (not second-hand) ones by age, sex and income group*.  
        - **Unit**: `PC` → **percentage of people** concerned (*only `unit = PC` is kept*).  
        - **Frequency**: `A` → annual.  
        """
    )

    # -------------------------------
    # DATASET PREVIEW
    # -------------------------------
    st.subheader("Dataset preview")
    st.dataframe(df.sample(20, random_state=42))

    # -------------------------------
    # DATA COVERAGE
    # -------------------------------
    st.subheader("Coverage & time period")
    years = sorted(pd.Series(df.get("year")).dropna().unique().tolist())
    countries = sorted(pd.Series(df.get("geo")).dropna().unique().tolist())
    incomes = sorted(pd.Series(df.get("incgrp_label")).dropna().unique().tolist()) if "incgrp_label" in df.columns else []
    ages = sorted(pd.Series(df.get("age_bucket_label")).dropna().unique().tolist()) if "age_bucket_label" in df.columns else []
    st.markdown(
        f"""
        - **Time span**: {years[0] if years else "?"} → {years[-1] if years else "?"}  
        - **Number of countries**: {len(countries)}  
        - **Income groups available**: {", ".join(incomes) if incomes else "—"}  
        - **Age groups (buckets)**: {", ".join(ages) if ages else "—"}
        """
    )

    # -------------------------------
    # COLUMN MEANING
    # -------------------------------
    st.subheader("Column definitions (in this project)")
    st.markdown(
        """
        | Column           | Meaning |
        |------------------|---------|
        | `DATAFLOW`       | Eurostat technical identifier (traceability). |
        | `LAST UPDATE`    | Last update timestamp from Eurostat (not used). |
        | `freq`           | Frequency (`A` = annual). |
        | `unit`           | Unit (`PC` = percentage). |
        | `geo`            | Country (ISO-2 code: FR, DE, IT…). |
        | `TIME_PERIOD`    | Year as text → converted to `year` (integer). |
        | `year`           | Year (integer) used in charts. |
        | `OBS_VALUE`      | % of people declaring they cannot afford to buy new clothes. |
        | `sex`            | Raw sex code: `M`, `F`, `T`. |
        | `sex_label`      | Human-readable: Men, Women, Total. |
        | `age`            | Raw age code (may vary by country/year). |
        | `age_bucket_label` | Standardized 9 age groups: Total, <18, 18–24, 25–34, 35–44, 45–54, 55–64, 65–74, ≥75. |
        | `incgrp`         | Income group raw code (`A_MD60`, `B_MD60`, `TOTAL`). |
        | `incgrp_label`   | Income group readable: Below 60% median (`B_MD60`), Above 60% median (`A_MD60`), Total. |
        | `iso3`           | ISO-3 country code (needed for the choropleth map). |
        | `OBS_FLAG`       | Data quality flag (empty in this dataset). |
        | `CONF_STATUS`    | Confidence status (empty in this dataset). |
        """
    )

    st.info(
        "**Age:** Eurostat provides heterogeneous codes depending on country and year. "
        "To avoid an endless list, all variants were automatically grouped "
        "into 9 standardized buckets (`age_bucket_label`)."
    )


    # -------------------------------
    # FILTERS
    # -------------------------------
    st.subheader("Application filters (sidebar)")
    st.markdown(
        """
        **Filter logic**: all filters are applied with a logical **AND** (country ∩ gender ∩ age ∩ income).  
        - **Country** (`geo`) — multi-select of ISO-2 codes.  
        - **Gender** (`sex_label`) — `Total`, `Women`, `Men`.  
        - **Age** (`age_bucket_label`) — **9 standardized categories**: `Total`, `<18`, `18–24`, `25–34`, `35–44`, `45–54`, `55–64`, `65–74`, `≥75`.  
        - **Income group** (`incgrp_label`) — `Below 60% of median income — poor households`, `≥60% of median income — non-poor households`, `Total population`.  
        - **Year** (`year`) — used for the **map** and **ranking**; time series always show the full span.
        """
    )

    st.subheader("Dashboard structure")
    st.markdown(
        """
        1. **Overview** — KPIs, country time series, **annual map**, ranking.  
        2. **Detailed analyses** — gender gap, **age** and **income** gradients, country focus.  
        3. **Conclusions** — key takeaways, limitations, policy implications.
        """
    )
