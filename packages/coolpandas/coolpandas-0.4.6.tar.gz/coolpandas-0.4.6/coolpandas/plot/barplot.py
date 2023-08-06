"""Barplot module."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .style import custom_template, format_title


def barplot(
    data_frame: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    title: str = "",
    subtitle: str | None = None,
    **kwargs,
) -> go.Figure:
    """Create a bar plot.

    Args:
        data_frame (pd.DataFrame): DataFrame to plot.
        x_axis (str): Column to use as x axis.
        y_axis (str): Column to use as y axis.
        title (str): Title of the plot.
        subtitle (str, optional): Subtitle of the plot. Defaults to None.
        **kwargs: Keyword arguments to pass to plotly.express.bar.

    Returns:
        go.Figure: Bar plot figure.
    """
    fig = px.bar(
        data_frame,
        x=x_axis,
        y=y_axis,
        title=format_title(title, subtitle=subtitle),
        template=custom_template,
        width=800,
        height=400,
        **kwargs,
    )
    fig.update_traces(width=0.5)
    return fig
