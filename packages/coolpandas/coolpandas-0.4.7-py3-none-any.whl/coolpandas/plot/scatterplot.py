"""Scatterplot module."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .style import custom_template, format_title


def scatterplot(
    data_frame: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    title: str = "",
    subtitle: str | None = None,
    **kwargs,
) -> go.Figure:
    """Create a scatter plot.

    Args:
        data_frame (pd.DataFrame): DataFrame to plot.
        x_axis (str): Column to use as x axis.
        y_axis (str): Column to use as y axis.
        title (str): Title of the plot.
        subtitle (str, optional): Subtitle of the plot. Defaults to None.
        **kwargs: Keyword arguments to pass to plotly.express.scatter.

    Returns:
        go.Figure: Scatter plot figure.
    """
    fig = px.scatter(
        data_frame,
        x=x_axis,
        y=y_axis,
        title=format_title(title, subtitle=subtitle),
        template=custom_template,
        width=800,
        height=400,
        **kwargs,
    )
    return fig
