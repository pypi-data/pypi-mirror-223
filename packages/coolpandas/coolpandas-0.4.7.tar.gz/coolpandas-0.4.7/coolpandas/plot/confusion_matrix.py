import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go

from .style import custom_template, format_title


def confusion_matrix(
    data_frame: pd.DataFrame,
    **kwargs,
) -> go.Figure:
    """Create a confusion matrix plot.

    Args:
        data_frame (pd.DataFrame): DataFrame to plot.
        **kwargs: Keyword arguments to pass to plotly.express.scatter_geo.

    Returns:
        go.Figure: Bar plot figure.
    """
    corr: pd.DataFrame = data_frame.corr()
    mask: np.ndarray = np.triu(np.ones_like(corr, dtype=bool))
    df_mask: pd.DataFrame = corr.mask(mask)
    correlations: list[float] = df_mask.values.tolist()
    correlations_text = [[str(round(y, 2)) for y in x] for x in correlations]

    fig = ff.create_annotated_heatmap(
        z=correlations,
        x=df_mask.columns.tolist(),
        y=df_mask.columns.tolist(),
        annotation_text=correlations_text,
        colorscale="agsunset",
        showscale=True,
        ygap=1,
        xgap=1,
        **kwargs,
    )
    fig.update_xaxes(side="bottom", automargin=True)
    fig.update_yaxes(automargin=True)
    fig.update_layout(
        title_text=format_title(
            title="Confusion matrix",
            subtitle=f"Pearson correlation between features and target (n={len(data_frame)})",
        ),
        width=1000,
        height=900,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        yaxis_autorange="reversed",
        template=custom_template,
    )

    for i in range(len(fig.layout.annotations)):
        if fig.layout.annotations[i].text == "nan":
            fig.layout.annotations[i].text = ""
    return fig
