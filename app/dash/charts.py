"""Reusable Plotly figure creation functions and Dash app creation.

As the project grows, add functions here that construct and return Plotly
figures for various economic datasets.  Keeping chart definitions separate
makes it easy to test and reuse them across different pages.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html


def sample_chart():
    """Return a simple line chart illustrating GDP growth over time.

    This sample uses synthetic data for demonstration.  In practice you
    should replace this with real economic time series (e.g. from FRED).

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly figure object ready for use in a Dash `dcc.Graph`.
    """
    # Synthetic data: annual GDP growth for demonstration.
    data = {
        "Year": [2018, 2019, 2020, 2021, 2022, 2023],
        "GDP Growth (%)": [2.9, 2.3, -3.4, 5.7, 1.6, 2.2],
    }
    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Year",
        y="GDP Growth (%)",
        title="Sample GDP Growth (synthetic data)",
        markers=True,
    )

    # Configure axes and layout aesthetics
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="GDP Growth (%)",
        template="plotly_white",
        height=400,
    )

    return fig


def create_dash_app():
    """Create and configure a Dash application with economic charts.
    
    Returns
    -------
    dash.Dash
        A configured Dash application instance.
    """
    # Create Dash app
    dash_app = dash.Dash(__name__, url_base_pathname='/dash/')
    
    # Get the sample chart figure
    fig = sample_chart()
    
    # Define the layout
    dash_app.layout = html.Div([
        html.H1("Economic Data Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
        
        html.Div([
            dcc.Graph(
                id='gdp-chart',
                figure=fig,
                style={'height': '500px'}
            )
        ], style={'margin': '20px'}),
        
        html.Div([
            html.P("This dashboard displays economic indicators and trends. "
                   "More charts and data sources will be added in future updates.",
                   style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 16})
        ], style={'margin': '20px'})
    ])
    
    return dash_app
