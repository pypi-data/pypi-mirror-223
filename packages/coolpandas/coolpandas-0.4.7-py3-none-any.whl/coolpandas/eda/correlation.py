import math

import pandas as pd
from plotly.graph_objs import Figure

from coolpandas.plot import confusion_matrix


def get_correlation(
    data_frame: pd.DataFrame, method: str = "pearson", plot: bool = True, **kwargs
) -> tuple[pd.DataFrame, Figure | None]:
    """Get the correlations of a DataFrame.

    Args:
        data_frame (pd.DataFrame): DataFrame to get correlations from.
        method (str, optional): Correlation method. Defaults to "pearson".
        plot (bool, optional): Plot the correlation map. Defaults to True.
        **kwargs: Keyword arguments to pass to pandas.DataFrame.corr.

    Returns:
        pd.DataFrame: Correlations.
    """
    correlation_matrix: pd.DataFrame = data_frame.corr(method=method)
    truncate: callable = lambda x: math.trunc(100 * x) / 100
    correlation_matrix = correlation_matrix.applymap(truncate)
    if plot:
        fig: Figure = confusion_matrix(data_frame, **kwargs)
        return correlation_matrix, fig
    return correlation_matrix, None
