# utils/viz.py
import pandas as pd
import plotly.express as px
import streamlit as st

def line_timeseries(df: pd.DataFrame, title: str):
    fig = px.line(
        df, x="year", y="obs_value", color="geo",
        markers=True,
        labels={"year":"Année","obs_value":"% personnes concernées","geo":"Pays"},
        title=title
    )
    st.plotly_chart(fig, use_container_width=True)

def choropleth_map(df: pd.DataFrame, title: str):
    fig = px.choropleth(
        df, locations="iso3", color="obs_value",
        color_continuous_scale="Reds",
        labels={"obs_value":"% privation vestimentaire"},
        title=title
    )
    st.plotly_chart(fig, use_container_width=True)

def bar_ranking(df: pd.DataFrame, n: int, title: str):
    d = df.dropna(subset=["obs_value"]).sort_values("obs_value", ascending=False).head(n)[::-1]
    fig = px.bar(
        d, x="obs_value", y="geo", orientation="h",
        labels={"obs_value":"%","geo":"Pays"},
        title=title
    )
    st.plotly_chart(fig, use_container_width=True)
