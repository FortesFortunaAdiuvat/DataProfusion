"""Reusable Plotly figure creation functions.

As the project grows, add functions here that construct and return Plotly
figures for various economic datasets.  Keeping chart definitions separate
makes it easy to test and reuse them across different pages.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px


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