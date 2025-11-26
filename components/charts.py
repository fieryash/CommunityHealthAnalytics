import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd

def plot_steps_timeline(activity_df):
    """
    Plots steps over time.
    """
    fig = px.line(activity_df, x='date', y='steps', title='Steps Timeline', markers=True)
    fig.update_traces(line_color='#FF4B4B')
    return fig

def plot_gym_timeline(activity_df):
    """
    Plots gym minutes over time.
    """
    fig = px.bar(activity_df, x='date', y='gym_minutes', title='Gym Minutes Timeline')
    fig.update_traces(marker_color='#00CC96')
    return fig

def plot_macro_breakdown(macros):
    """
    Pie chart for macros.
    macros: {'Protein': 150, 'Carbs': 200, 'Fat': 60}
    """
    labels = list(macros.keys())
    values = list(macros.values())
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text="Macro Breakdown")
    return fig

def plot_tower_comparison(tower_stats_df):
    """
    Bar chart comparing tower scores.
    """
    fig = px.bar(
        tower_stats_df, 
        x='tower_id', 
        y='health_score', 
        color='health_score',
        title='Tower Health Scores',
        color_continuous_scale='RdYlGn'
    )
    return fig
