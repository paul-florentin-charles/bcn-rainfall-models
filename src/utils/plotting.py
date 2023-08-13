"""
Provides useful functions for plotting rainfall data in all shapes.
"""
from typing import Optional

import pandas as pd
from matplotlib import pyplot as plt

from src.enums.labels import Label


def plot_column_according_to_year(yearly_rainfall: pd.DataFrame,
                                  label: Label,
                                  color: Optional[str] = None) -> bool:
    """
    Plot specified column data according to year.

    :param color:
    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be plotted as y-values.
    :return: A boolean set to True if data has been successfully plotted, False otherwise.
    """
    if Label.YEAR not in yearly_rainfall.columns or label not in yearly_rainfall.columns:
        return False

    plt.plot(yearly_rainfall[Label.YEAR.value],
             yearly_rainfall[label.value],
             label=label.value,
             c=color)

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
    if Label.YEAR not in yearly_rainfall.columns or label not in yearly_rainfall.columns:
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
    if Label.YEAR not in yearly_rainfall.columns or label not in yearly_rainfall.columns:
        return False

    plt.bar(yearly_rainfall[Label.YEAR.value],
            yearly_rainfall[label.value],
            label=label.value)

    return True


def bar_monthly_rainfall_averages(monthly_rainfalls: list) -> list:
    """
    Plots a bar graphic displaying average rainfall for each month passed through the list.

    :param monthly_rainfalls: A list of instances of MonthlyRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :return: A list of the Rainfall averages for each month.
    """
    month_labels, averages = [], []
    for monthly_rainfall in monthly_rainfalls:
        month_labels.append(monthly_rainfall.month.name[:3])
        averages.append(monthly_rainfall.get_average_yearly_rainfall())

    plt.bar(month_labels, averages, label='Average rainfall (mm)')
    plt.legend()

    return averages


def bar_monthly_rainfall_linreg_slopes(monthly_rainfalls: list) -> list:
    """
    Plots a bar graphic displaying linear regression slope for each month passed through the list.

    :param monthly_rainfalls: A list of instances of MonthlyRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :return: A list of the Rainfall LinReg slopes for each month.
    """
    month_labels, slopes = [], []
    for monthly_rainfall in monthly_rainfalls:
        month_labels.append(monthly_rainfall.month.name[:3])
        slopes.append(monthly_rainfall.add_linear_regression()[1])

    plt.bar(month_labels, slopes, label='Linear Regression slope (mm/year)')
    plt.legend()

    return slopes
