# sections/deep_dives.py
import streamlit as st
import pandas as pd
import plotly.express as px

def render(df_full: pd.DataFrame, tables: dict, filters: dict):
    """
    Deep Dives page.
    Uses df_full (raw loaded data), not the already-filtered df, so that we can
    deliberately IGNORE sidebar Sex/Age/Income filters and compare those groups.
    We still respect Country selection (geo) and the selected year for year-specific charts.
    """
    st.header("Deep Dives — Gender, Age & Income Analysis")

    if df_full.empty:
        st.warning("No data available.")
        return

    # ------------------------------------------------------------
    # Build a base df that only respects COUNTRY selection (geo)
    # ------------------------------------------------------------
    base = df_full.copy()
    if filters.get("geo"):
        base = base[base["geo"].isin(filters["geo"])]

    # Helper: year slice for “selected-year” charts
    year_selected = filters.get("year_for_map", None)
    base_year = base[base["year"] == year_selected] if year_selected in base["year"].unique() else pd.DataFrame()

    # -----------------------------------------
    # Local controls (specific to Deep Dives)
    # -----------------------------------------
    with st.expander("Deep-dive controls (override sidebar group filters)"):
        # Gender options present
        genders_all = sorted(base["sex_label"].dropna().unique()) if "sex_label" in base.columns else []
        genders_pick = st.multiselect(
            "Genders to compare", genders_all,
            default=[g for g in ["Women", "Men"] if g in genders_all]
        )

        # Age buckets present
        ages_all = ["Total","<18","18-24","25-34","35-44","45-54","55-64","65-74","≥75"]
        ages_present = [a for a in ages_all if a in set(base.get("age_bucket_label", []))]
        age_pick = st.multiselect(
            "Age groups to compare",
            ages_present,
            default=[a for a in ages_present if a != "Total"][:8] or ages_present
        )

        # Income
        inc_all = sorted(base["incgrp_label"].dropna().unique()) if "incgrp_label" in base.columns else []
        inc_pick = st.multiselect(
            "Income groups to compare", inc_all,
            default=[i for i in ['≥ 60% of median income — non-poor','< 60% of median income — at-risk-of-poverty'] if i in inc_all]
        )

    # If user empties a control, keep all present (avoid blank charts)
    if not genders_pick: genders_pick = genders_all
    if not age_pick: age_pick = ages_present
    if not inc_pick: inc_pick = inc_all

    # Filter for local picks (but NOT by sidebar sex/age/inc)
    df_gender = base[base["sex_label"].isin(genders_pick)] if "sex_label" in base.columns else pd.DataFrame()
    df_age    = base[base["age_bucket_label"].isin(age_pick)] if "age_bucket_label" in base.columns else pd.DataFrame()
    df_inc    = base[base["incgrp_label"].isin(inc_pick)] if "incgrp_label" in base.columns else pd.DataFrame()

    # ============================================================
    # 1) GENDER
    # ============================================================
    st.subheader("👩‍🧑 Gender comparison")

    if not df_gender.empty:
        # Average by gender (all years in selection)
        gender_avg = df_gender.groupby("sex_label", as_index=False)["obs_value"].mean()
        fig_gender = px.bar(
            gender_avg, x="sex_label", y="obs_value", color="sex_label",
            text_auto=".1f",
            labels={"sex_label": "Gender", "obs_value": "% deprived"},
            title="Average clothing deprivation by gender (all years, selected countries)"
        )
        st.plotly_chart(fig_gender, use_container_width=True)

        # Gender gap over time (Women - Men) if both exist
        if set(["year","sex_label"]).issubset(df_gender.columns):
            pivot = df_gender.pivot_table(index="year", columns="sex_label", values="obs_value", aggfunc="mean")
            if "Women" in pivot.columns and "Men" in pivot.columns:
                pivot["Gap (Women - Men)"] = pivot["Women"] - pivot["Men"]
                fig_gap = px.line(
                    pivot.reset_index(), x="year", y="Gap (Women - Men)", markers=True,
                    labels={"year":"Year", "Gap (Women - Men)":"Gap (percentage points)"},
                    title="Gender gap over time (Women minus Men)"
                )
                fig_gap.update_layout(hovermode="x unified")
                st.plotly_chart(fig_gap, use_container_width=True)
    else:
        st.info("No gender data available for the selected countries.")

    # ============================================================
    # 2) AGE
    # ============================================================
    st.subheader("🎂 Age groups")

    if not df_age.empty:
        # Average by age group (all years)
        age_avg = df_age.groupby("age_bucket_label", as_index=False)["obs_value"].mean()
        fig_age = px.bar(
            age_avg.sort_values("obs_value", ascending=False),
            x="obs_value", y="age_bucket_label", orientation="h",
            labels={"age_bucket_label":"Age group", "obs_value":"% deprived"},
            title="Average clothing deprivation by age group (all years, selected countries)"
        )
        st.plotly_chart(fig_age, use_container_width=True)

        # Time series for a chosen age bucket (local select)
        # Time series for a chosen age bucket (local select)
        choice_age = st.selectbox("Time trend for age group:", options=age_pick, index=0)

        age_ts_raw = df_age[df_age["age_bucket_label"] == choice_age]
        if not age_ts_raw.empty:
            age_ts = (
                age_ts_raw
                .groupby(["geo", "year"], as_index=False)["obs_value"]
                .mean()
            )

            fig_age_ts = px.line(
                age_ts,
                x="year",
                y="obs_value",
                color="geo",
                markers=True,
                labels={"year": "Year", "obs_value": "% deprived", "geo": "Country"},
                title=f"Trend over time — {choice_age} (selected countries; averaged across gender & income)"
            )
            fig_age_ts.update_layout(hovermode="x unified")
            st.plotly_chart(fig_age_ts, use_container_width=True)
        else:
            st.info("No data for the selected age group in the selected countries.")


    # ============================================================
    # 3) INCOME
    # ============================================================
    st.subheader("💸 Income groups")

    if not df_inc.empty:
        # Average by income group (all years)
        inc_avg = df_inc.groupby("incgrp_label", as_index=False)["obs_value"].mean()
        fig_inc = px.bar(
            inc_avg, x="incgrp_label", y="obs_value", color="incgrp_label", text_auto=".1f",
            labels={"incgrp_label":"Income group","obs_value":"% deprived"},
            title="Average clothing deprivation by income group (all years, selected countries)"
        )
        st.plotly_chart(fig_inc, use_container_width=True)

        # Box plot (distribution by income group, all years)
        fig_inc_box = px.box(
            df_inc, x="incgrp_label", y="obs_value", points="all", color="incgrp_label",
            labels={"incgrp_label":"Income group","obs_value":"% deprived"},
            title="Distribution by income group (all years, selected countries)"
        )
        st.plotly_chart(fig_inc_box, use_container_width=True)

        # Time series by income group
        fig_inc_ts = px.line(
            df_inc, x="year", y="obs_value", color="incgrp_label", markers=True,
            labels={"incgrp_label":"Income group","obs_value":"% deprived","year":"Year"},
            title="Trend over time by income group (selected countries)"
        )
        fig_inc_ts.update_layout(hovermode="x unified")
        st.plotly_chart(fig_inc_ts, use_container_width=True)
    else:
        st.info("No income data available for the selected countries.")

    # ============================================================
    # Simple auto-takeaways
    # ============================================================
    st.subheader("✨ Key takeaways (auto)")
    try:
        # Gender gap quick stat
        g_means = df_gender.groupby("sex_label")["obs_value"].mean()
        if {"Women","Men"}.issubset(g_means.index):
            st.markdown(f"- **Gender gap:** Women report **{(g_means['Women']-g_means['Men']):.1f} pp** higher deprivation on average.")
        # Most deprived age
        if not df_age.empty:
            worst_age = df_age.groupby("age_bucket_label")["obs_value"].mean().idxmax()
            st.markdown(f"- **Most affected age group:** **{worst_age}** on average.")
        # Income effect
        if not df_inc.empty:
            poor = df_inc[df_inc["incgrp_label"].str.contains("Below", case=False)]["obs_value"].mean()
            nonpoor = df_inc[df_inc["incgrp_label"].str.contains("≥", case=False)]["obs_value"].mean()
            if pd.notna(poor) and pd.notna(nonpoor):
                st.markdown(f"- **Income effect:** Below-60% median group is **{(poor-nonpoor):.1f} pp** higher than ≥60% median.")
    except Exception:
        pass

    # ============================================================
    # Download data used on this page
    # ============================================================
    st.subheader("⬇️ Download data used in this page")
    st.download_button(
        "Download CSV (deep-dives basis; country-only filtered)",
        base.to_csv(index=False).encode("utf-8"),
        file_name="deep_dives_base.csv",
        mime="text/csv"
    )
