"""
Provides useful functions for plotting rainfall data in all shapes.
"""

import pandas as pd
from matplotlib import pyplot as plt

from src.enums.labels import Label


def plot_column_according_to_year(yearly_rainfall: pd.DataFrame, label: Label) -> bool:
    """
    Plot specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be plotted as y-values.
    :return: A boolean set to True if data has been successfully plotted, False otherwise.
    """
    if (yearly_rainfall is None
            or Label.YEAR not in yearly_rainfall.columns
            or label not in yearly_rainfall.columns):
        return False

    plt.plot(yearly_rainfall[Label.YEAR.value],
             yearly_rainfall[label.value],
             label=label.value)

    return True


def scatter_column_according_to_year(yearly_rainfall: pd.DataFrame,
                                     label: Label,
                                     display_label: bool = True) -> bool:
    """
    Scatter specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be scattered as y-values.
    :param display_label: Whether to display label or not. Default to True (optional)
    :return: A boolean set to True if data has been successfully plotted, False otherwise.
    """
    if (yearly_rainfall is None
            or Label.YEAR not in yearly_rainfall.columns
            or label not in yearly_rainfall.columns):
        return False

    label_value: str = label.value if display_label else None
    plt.scatter(yearly_rainfall[Label.YEAR.value],
                yearly_rainfall[label.value],
                label=label_value)

    return True


def bar_column_according_to_year(yearly_rainfall: pd.DataFrame, label: Label) -> bool:
    """
    Plot bars for specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be displayed as bars for y-values.
    :return: A boolean set to True if data has been successfully plotted, False otherwise.
    """
    if (yearly_rainfall is None
            or Label.YEAR not in yearly_rainfall.columns
            or label not in yearly_rainfall.columns):
        return False

    plt.bar(yearly_rainfall[Label.YEAR.value],
            yearly_rainfall[label.value],
            label=label.value)

    return True
