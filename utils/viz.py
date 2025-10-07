import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_city_map(city_stats):
    """
    Create a bar chart showing depression rates by city
    Only shows cities that meet minimum student threshold
    
    Args:
        city_stats: DataFrame with city statistics (already filtered)
        
    Returns:
        plotly figure
    """
    # Sort by depression rate (ascending for horizontal bar chart)
    city_stats_sorted = city_stats.sort_values('Depression_Rate', ascending=True)
    
    fig = px.bar(
        city_stats_sorted,
        x='Depression_Rate',
        y='City',
        orientation='h',
        title=f'Depression Rate by City ({len(city_stats_sorted)} Cities)',
        labels={'Depression_Rate': 'Depression Rate (%)', 'City': 'City'},
        color='Depression_Rate',
        color_continuous_scale='OrRd',
        text='Depression_Rate'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside',
        textfont=dict(size=10, color='black'),
        hovertemplate='<b>%{y}</b><br>Depression Rate: %{x:.1f}%<br>Students: %{customdata[0]}<extra></extra>',
        customdata=city_stats_sorted[['Total_Students']]
    )
    
    fig.update_layout(
        height=max(600, len(city_stats_sorted) * 25),  # Dynamic height
        showlegend=False,
        xaxis_title="Depression Rate (%)",
        yaxis_title="City",
        xaxis=dict(range=[0, 105])
    )
    
    return fig


def create_demographic_chart(demo_stats, category='gender'):
    """
    Create bar chart for demographic comparisons
    
    Args:
        demo_stats: Dictionary with demographic statistics
        category: 'gender' or 'degree'
        
    Returns:
        plotly figure
    """
    df = demo_stats[category]
    
    fig = px.bar(
        df,
        x=category.capitalize(),
        y='Depression_Rate',
        title=f'Depression Rate by {category.capitalize()}',
        labels={'Depression_Rate': 'Depression Rate (%)', category.capitalize(): category.capitalize()},
        color='Depression_Rate',
        color_continuous_scale='OrRd',
        text='Depression_Rate'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside',
        textfont=dict(size=14, color='black')
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title=category.capitalize(),
        yaxis_title="Depression Rate (%)",
        yaxis=dict(range=[0, max(df['Depression_Rate']) * 1.15]),
        height=500
    )
    
    return fig


def create_sleep_chart(sleep_stats):
    """
    Create chart showing relationship between sleep and depression
    
    Args:
        sleep_stats: DataFrame with sleep statistics
        
    Returns:
        plotly figure
    """
    fig = px.bar(
        sleep_stats,
        x='Sleep_Duration',
        y='Depression_Rate',
        title='Depression Rate by Sleep Duration',
        labels={'Depression_Rate': 'Depression Rate (%)', 'Sleep_Duration': 'Sleep Duration'},
        color='Depression_Rate',
        color_continuous_scale='OrRd',
        text='Depression_Rate'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside',
        textfont=dict(size=14, color='black')
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title="Sleep Duration",
        yaxis_title="Depression Rate (%)",
        yaxis=dict(range=[0, max(sleep_stats['Depression_Rate']) * 1.15]),
        height=500
    )
    
    return fig


def create_correlation_heatmap(df):
    """
    Create correlation heatmap for numeric variables
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        plotly figure
    """
    # Select only numeric columns relevant for correlation
    numeric_cols = ['Age', 'Academic_Pressure', 'CGPA', 'Study_Satisfaction', 
                    'Financial_Stress', 'Work_Study_Hours', 'Depression']
    
    # Filter to existing columns
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        title='Correlation Matrix: Key Variables',
        labels=dict(color="Correlation"),
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1,
        text_auto='.2f'
    )
    
    fig.update_layout(
        width=700,
        height=600
    )
    
    return fig


def create_distribution_chart(df, column, title):
    """
    Create histogram for variable distribution
    
    Args:
        df: DataFrame
        column: Column name to plot
        title: Chart title
        
    Returns:
        plotly figure
    """
    fig = px.histogram(
        df,
        x=column,
        color='Depression',
        title=title,
        labels={column: column, 'Depression': 'Depression Status'},
        barmode='overlay',
        opacity=0.7,
        color_discrete_map={0: 'lightblue', 1: 'red'}
    )
    
    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count",
        legend_title="Depression"
    )
    
    return fig