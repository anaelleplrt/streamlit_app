"""
Visualization utilities for consistent chart styling
Uses Plotly for interactive charts
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, List


# Consistent color scheme
COLORS = {
    'primary': '#2563eb',      # Blue
    'secondary': '#7c3aed',    # Purple
    'success': '#10b981',      # Green
    'warning': '#f59e0b',      # Orange
    'danger': '#ef4444',       # Red
    'neutral': '#6b7280',      # Gray
    'income_scale': ['#ef4444', '#f59e0b', '#10b981'],  # Red (poor) to Green (rich)
    'disease_scale': px.colors.sequential.Reds
}


def create_income_inequality_chart(df: pd.DataFrame, disease: str, type_: str = 'prevalence') -> go.Figure:
    """Create bar chart showing rates by income decile"""
    data = df[
        (df['varTauxLib'] == disease) &
        (df['type'] == type_)
    ].copy()
    
    if data.empty or 'income_decile' not in data.columns:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for this disease",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(height=400)
        return fig
    
    data = data.sort_values('income_decile')
    
    # Color gradient
    n_deciles = len(data)
    if n_deciles <= 3:
        colors = ['#ef4444'] * n_deciles
    elif n_deciles <= 7:
        colors = ['#ef4444'] * 3 + ['#f59e0b'] * (n_deciles - 3)
    else:
        colors = ['#ef4444'] * 3 + ['#f59e0b'] * 4 + ['#10b981'] * (n_deciles - 7)
    
    fig = go.Figure()
    
    # CORRECT column names
    has_ci = 'txStandDirModBB' in data.columns and 'txStandDirModBH' in data.columns
    
    if has_ci:
        error_y = dict(
            type='data',
            symmetric=False,
            array=data['txStandDirModBH'] - data['txStandDir'],
            arrayminus=data['txStandDir'] - data['txStandDirModBB']
        )
    else:
        error_y = None
    
    fig.add_trace(go.Bar(
        x=data['income_decile'],
        y=data['txStandDir'],
        marker_color=colors,
        name='Rate',
        error_y=error_y,
        hovertemplate='<b>Decile %{x}</b><br>Rate: %{y:.1f}%<br><extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{disease} - {type_.capitalize()} by Income Decile",
        xaxis_title="Income Decile (1=Poorest, 10=Richest)",
        yaxis_title=f"{type_.capitalize()} Rate (%)",
        hovermode='closest',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig


def create_comparison_chart(df: pd.DataFrame, disease: str, group_col: str, 
                           type_: str = 'prevalence', top_n: int = 10) -> go.Figure:
    """
    Create horizontal bar chart comparing groups (regions, education, etc.)
    
    Args:
        df: Grouped table
        disease: Disease name
        group_col: Column name for grouping
        type_: 'prevalence' or 'incidence'
        top_n: Number of top groups to show
        
    Returns:
        Plotly figure
    """
    data = df[
        (df['varTauxLib'] == disease) &
        (df['type'] == type_)
    ].copy()
    
    if data.empty or group_col not in data.columns:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No {group_col} data available for this disease",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(height=400)
        return fig
    
    # Get top N by rate
    data = data.nlargest(min(top_n, len(data)), 'txStandDir')
    data = data.sort_values('txStandDir')
    
    fig = go.Figure()
    
    # Check if confidence intervals exist
    has_ci = 'txStandDirBB' in data.columns and 'txStandDirBH' in data.columns
    
    if has_ci:
        error_x = dict(
            type='data',
            symmetric=False,
            array=data['txStandDirBH'] - data['txStandDir'],
            arrayminus=data['txStandDir'] - data['txStandDirBB']
        )
    else:
        error_x = None
    
    fig.add_trace(go.Bar(
        x=data['txStandDir'],
        y=data[group_col],
        orientation='h',
        marker_color=COLORS['primary'],
        error_x=error_x,
        hovertemplate='<b>%{y}</b><br>' +
                      'Rate: %{x:.1f}%<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{disease} - {type_.capitalize()} by {group_col.replace('_', ' ').title()}",
        xaxis_title=f"{type_.capitalize()} Rate (%)",
        yaxis_title="",
        template='plotly_white',
        height=max(400, len(data) * 30),
        showlegend=False
    )
    
    return fig


def create_multiple_diseases_chart(df: pd.DataFrame, diseases: List[str], 
                                   group_col: str = 'income_decile',
                                   type_: str = 'prevalence') -> go.Figure:
    """
    Create grouped bar chart comparing multiple diseases
    
    Args:
        df: Income or other grouped table
        diseases: List of disease names
        group_col: Column to group by
        type_: 'prevalence' or 'incidence'
        
    Returns:
        Plotly figure
    """
    if not diseases:
        fig = go.Figure()
        fig.add_annotation(
            text="No diseases selected",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = go.Figure()
    
    for i, disease in enumerate(diseases):
        data = df[
            (df['varTauxLib'] == disease) &
            (df['type'] == type_)
        ].copy()
        
        if not data.empty and group_col in data.columns:
            data = data.sort_values(group_col)
            
            fig.add_trace(go.Bar(
                x=data[group_col],
                y=data['txStandDir'],
                name=disease[:40] + '...' if len(disease) > 40 else disease,  # Truncate long names
                marker_color=px.colors.qualitative.Set2[i % len(px.colors.qualitative.Set2)],
                hovertemplate='<b>%{fullData.name}</b><br>' +
                              f'{group_col}: %{{x}}<br>' +
                              'Rate: %{y:.1f}%<br>' +
                              '<extra></extra>'
            ))
    
    if len(fig.data) == 0:
        fig.add_annotation(
            text="No data available for selected diseases",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig.update_layout(
        title=f"Comparison of {type_.capitalize()} Rates Across Diseases",
        xaxis_title=group_col.replace('_', ' ').title(),
        yaxis_title=f"{type_.capitalize()} Rate (%)",
        barmode='group',
        template='plotly_white',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_heatmap(df: pd.DataFrame, diseases: List[str], type_: str = 'prevalence') -> go.Figure:
    """
    Create heatmap showing disease rates across income deciles
    
    Args:
        df: Income table
        diseases: List of diseases
        type_: 'prevalence' or 'incidence'
        
    Returns:
        Plotly figure
    """
    if not diseases:
        fig = go.Figure()
        fig.add_annotation(
            text="No diseases selected for heatmap",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    pivot_data = []
    
    for disease in diseases:
        data = df[
            (df['varTauxLib'] == disease) &
            (df['type'] == type_)
        ].copy()
        
        if not data.empty and 'income_decile' in data.columns:
            data = data.sort_values('income_decile')
            row = {'disease': disease[:40] + '...' if len(disease) > 40 else disease}
            for _, r in data.iterrows():
                decile = int(r['income_decile'])
                row[f"D{decile}"] = r['txStandDir']
            pivot_data.append(row)
    
    if not pivot_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for heatmap",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    pivot_df = pd.DataFrame(pivot_data).set_index('disease')
    
    # Fill missing values with NaN for cleaner display
    pivot_df = pivot_df.reindex(columns=[f"D{i}" for i in range(1, 11)], fill_value=np.nan)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='Reds',
        hovertemplate='Disease: %{y}<br>Decile: %{x}<br>Rate: %{z:.1f}%<extra></extra>',
        colorbar=dict(title="Rate (%)")
    ))
    
    fig.update_layout(
        title=f"Disease {type_.capitalize()} Heatmap by Income Decile",
        xaxis_title="Income Decile",
        yaxis_title="Disease",
        template='plotly_white',
        height=max(400, len(diseases) * 40)
    )
    
    return fig


def create_inequality_ratio_chart(ratios: pd.DataFrame) -> go.Figure:
    """
    Create chart showing inequality ratios (D1/D10)
    Higher ratio = more inequality
    
    Args:
        ratios: DataFrame with columns ['disease', 'ratio']
        
    Returns:
        Plotly figure
    """
    if ratios.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No inequality ratios available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    ratios = ratios.copy()
    ratios = ratios.sort_values('ratio', ascending=True)
    
    # Truncate long disease names
    ratios['disease_short'] = ratios['disease'].apply(
        lambda x: x[:40] + '...' if len(x) > 40 else x
    )
    
    # Color based on inequality level
    colors = []
    for r in ratios['ratio']:
        if r < 1.5:
            colors.append('#10b981')  # Green - low inequality
        elif r < 2.5:
            colors.append('#f59e0b')  # Orange - moderate
        else:
            colors.append('#ef4444')  # Red - high inequality
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=ratios['ratio'],
        y=ratios['disease_short'],
        orientation='h',
        marker_color=colors,
        hovertemplate='<b>%{y}</b><br>' +
                      'Inequality Ratio: %{x:.2f}x<br>' +
                      '<extra></extra>'
    ))
    
    # Add reference line at 1.0 (equality)
    fig.add_vline(x=1.0, line_dash="dash", line_color="gray", 
                  annotation_text="Equality", annotation_position="top right")
    
    fig.update_layout(
        title="Disease Inequality Rankings: Poorest vs Richest (D1/D10 Ratio)",
        xaxis_title="Inequality Ratio (Higher = More Unequal)",
        yaxis_title="",
        template='plotly_white',
        height=max(400, len(ratios) * 30),
        showlegend=False
    )
    
    return fig


def create_timeseries_chart(df: pd.DataFrame, diseases: List[str], 
                           type_: str = 'prevalence') -> go.Figure:
    """
    Create time series line chart
    
    Args:
        df: Time series table
        diseases: List of diseases
        type_: 'prevalence' or 'incidence'
        
    Returns:
        Plotly figure
    """
    if df.empty or not diseases:
        fig = go.Figure()
        fig.add_annotation(
            text="No time series data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = go.Figure()
    
    for i, disease in enumerate(diseases):
        data = df[
            (df['varTauxLib'] == disease) &
            (df['type'] == type_)
        ].copy()
        
        if not data.empty and 'year' in data.columns:
            data = data.sort_values('year')
            
            fig.add_trace(go.Scatter(
                x=data['year'],
                y=data['txStandDir'],
                mode='lines+markers',
                name=disease[:40] + '...' if len(disease) > 40 else disease,
                line=dict(width=2),
                marker=dict(size=6),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                              'Year: %{x}<br>' +
                              'Rate: %{y:.1f}%<br>' +
                              '<extra></extra>'
            ))
    
    if len(fig.data) == 0:
        fig.add_annotation(
            text="No data for selected diseases",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig.update_layout(
        title=f"{type_.capitalize()} Trends Over Time",
        xaxis_title="Year",
        yaxis_title=f"{type_.capitalize()} Rate (%)",
        template='plotly_white',
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format number as percentage
    
    Args:
        value: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}%"


def format_large_number(value: float) -> str:
    """
    Format large numbers with K, M suffixes
    
    Args:
        value: Number to format
        
    Returns:
        Formatted number string
    """
    if pd.isna(value):
        return "N/A"
    
    if value >= 1e6:
        return f"{value/1e6:.1f}M"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K"
    else:
        return f"{value:.0f}"


def create_empty_chart(message: str = "No data available") -> go.Figure:
    """
    Create an empty chart with a message
    
    Args:
        message: Message to display
        
    Returns:
        Empty Plotly figure with message
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )
    fig.update_layout(
        template='plotly_white',
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig