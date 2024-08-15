"""
Provides useful functions for plotting rainfall data in all shapes.
"""

import pandas as pd
from matplotlib import pyplot as plt

from src.core.utils.enums.labels import Label


def plot_column_according_to_year(
    yearly_rainfall: pd.DataFrame, label: Label, color: str | None = None
) -> bool:
    """
    Plot specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be plotted as y-values.
    :param color: A string to set plot colour (optional).
    :return: A boolean set to True if data has been successfully plotted, False otherwise.
    """
    if (
        Label.YEAR not in yearly_rainfall.columns
        or label not in yearly_rainfall.columns
    ):
        return False

    plt.plot(
        yearly_rainfall[Label.YEAR.value],
        yearly_rainfall[label.value],
        label=label.value,
        c=color,
    )

    return True


def scatter_column_according_to_year(
    yearly_rainfall: pd.DataFrame, label: Label, display_label=True
) -> bool:
    """
    Scatter specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be scattered as y-values.
    :param display_label: Whether to display label or not. Default to True (optional)
    :return: A boolean set to True if data has been successfully plotted, False otherwise.
    """
    if (
        Label.YEAR not in yearly_rainfall.columns
        or label not in yearly_rainfall.columns
    ):
        return False

    plt.scatter(
        yearly_rainfall[Label.YEAR.value],
        yearly_rainfall[label.value],
        label=label.value if display_label else None,
    )

    return True


def bar_column_according_to_year(yearly_rainfall: pd.DataFrame, label: Label) -> bool:
    """
    Plot bars for specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be displayed as bars for y-values.
    :return: A boolean set to True if data has been successfully plotted, False otherwise.
    """
    if (
        Label.YEAR not in yearly_rainfall.columns
        or label not in yearly_rainfall.columns
    ):
        return False

    plt.bar(
        yearly_rainfall[Label.YEAR.value],
        yearly_rainfall[label.value],
        label=label.value,
    )

    return True


def bar_monthly_rainfall_averages(
    monthly_rainfalls: list,
    *,
    begin_year: int,
    end_year: int | None = None,
    label="Average rainfall (mm)",
) -> list:
    """
    Plots a bar graphic displaying average rainfall for each month passed through the dict.

    :param monthly_rainfalls: A list of instances of MonthlyRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values (optional).
    :param label: A string to use as a label for bar graphic. (optional)
    Defaults to "Average rainfall (mm)".
    :return: A list of the Rainfall averages for each month.
    """
    month_labels, averages = [], []
    for monthly_rainfall in monthly_rainfalls:
        month_labels.append(monthly_rainfall.month.value[:3])
        averages.append(
            monthly_rainfall.get_average_yearly_rainfall(
                begin_year=begin_year, end_year=end_year
            )
        )

    plt.bar(month_labels, averages, label=label)
    plt.legend()

    return averages


def bar_monthly_rainfall_linreg_slopes(monthly_rainfalls: list) -> list:
    """
    Plots a bar graphic displaying linear regression slope for each month passed through the dict.

    :param monthly_rainfalls: A list of instances of MonthlyRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :return: A list of the Rainfall LinReg slopes for each month.
    """
    month_labels, slopes = [], []
    for monthly_rainfall in monthly_rainfalls:
        month_labels.append(monthly_rainfall.month.value[:3])
        slopes.append(monthly_rainfall.add_linear_regression()[1])

    plt.bar(month_labels, slopes, label="Linear Regression slope (mm/year)")
    plt.legend()

    return slopes


def bar_seasonal_rainfall_averages(
    seasonal_rainfalls: list,
    *,
    begin_year: int,
    end_year: int | None = None,
    label="Average rainfall (mm)",
) -> list:
    """
    Plots a bar graphic displaying average rainfall for each season passed through the dict.

    :param seasonal_rainfalls: A list of instances of SeasonalRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values (optional).
    :param label: A string to use as a label for bar graphic. (optional)
    Defaults to "Average rainfall (mm)".
    :return: A list of the Rainfall averages for each season.
    """
    season_labels, averages = [], []
    for seasonal_rainfall in seasonal_rainfalls:
        season_labels.append(seasonal_rainfall.season.value)
        averages.append(
            seasonal_rainfall.get_average_yearly_rainfall(
                begin_year=begin_year, end_year=end_year
            )
        )

    plt.bar(season_labels, averages, label=label)
    plt.legend()

    return averages


def bar_seasonal_rainfall_linreg_slopes(seasonal_rainfalls: list) -> list:
    """
    Plots a bar graphic displaying linear regression slope for each season passed through the dict.

    :param seasonal_rainfalls: A list of instances of SeasonalRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :return: A list of the Rainfall LinReg slopes for each season.
    """
    season_labels, slopes = [], []
    for seasonal_rainfall in seasonal_rainfalls:
        season_labels.append(seasonal_rainfall.season.value)
        slopes.append(seasonal_rainfall.add_linear_regression()[1])

    plt.bar(season_labels, slopes, label="Linear Regression slope (mm/year)")
    plt.legend()

    return slopes
