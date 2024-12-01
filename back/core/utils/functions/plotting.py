"""
Provides useful functions for plotting rainfall data in all shapes.
"""

import pandas as pd
import matplotlib.pyplot as plt

# import plotly.express as px
import plotly.graph_objs as go

from back.core.utils.enums import Label


def plot_column_according_to_year(
    yearly_rainfall: pd.DataFrame, label: Label, *, color: str | None = None
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
    yearly_rainfall: pd.DataFrame, label: Label, *, display_label=True
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


def get_bar_figure_of_column_according_to_year(
    yearly_rainfall: pd.DataFrame, label: Label, *, figure_label: str | None = None
) -> go.Figure | None:
    """
    Return plotly bar figure for specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be displayed as bars for y-values.
    :param figure_label: A string to label graphic data (optional).
    If not set or set to "", label value is used.
    :return: A plotly Figure object if data has been successfully plotted, None otherwise.
    """
    if (
        Label.YEAR not in yearly_rainfall.columns
        or label not in yearly_rainfall.columns
    ):
        return None

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x=yearly_rainfall[Label.YEAR.value],
            y=yearly_rainfall[label.value],
        )
    )

    figure.update_layout(title=figure_label or label.value)
    figure.update_xaxes(title_text=Label.YEAR.value)
    figure.update_yaxes(title_text=label.value)

    return figure


def get_bar_figure_of_monthly_rainfall_averages(
    monthly_rainfalls: list,
    *,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying average rainfall for each month passed through the dict.

    :param monthly_rainfalls: A list of instances of MonthlyRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall averages for each month.
    """
    month_labels: list[str] = []
    averages: list[float] = []
    for monthly_rainfall in monthly_rainfalls:
        month_labels.append(monthly_rainfall.month.value)
        averages.append(
            monthly_rainfall.get_average_yearly_rainfall(
                begin_year=begin_year, end_year=end_year
            )
        )

    figure = go.Figure()
    figure.add_trace(go.Bar(x=month_labels, y=averages, name="Monthly"))

    figure.update_layout(
        title=f"Average monthly rainfall (mm) between {begin_year} and {end_year}"
    )
    figure.update_xaxes(title_text="Month")
    figure.update_yaxes(title_text=Label.RAINFALL.value)

    return figure


def get_bar_figure_of_seasonal_rainfall_averages(
    seasonal_rainfalls: list,
    *,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying average rainfall for each season passed through the dict.

    :param seasonal_rainfalls: A list of instances of SeasonalRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall averages for each season.
    """
    season_labels: list[str] = []
    averages: list[float] = []
    for seasonal_rainfall in seasonal_rainfalls:
        season_labels.append(seasonal_rainfall.season.value)
        averages.append(
            seasonal_rainfall.get_average_yearly_rainfall(
                begin_year=begin_year, end_year=end_year
            )
        )

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x=season_labels,
            y=averages,
            name="Seasonal",
        )
    )

    figure.update_layout(
        title=f"Average seasonal rainfall (mm) between {begin_year} and {end_year}"
    )
    figure.update_xaxes(title_text="Season")
    figure.update_yaxes(title_text=Label.RAINFALL.value)

    return figure


def get_bar_figure_of_monthly_rainfall_linreg_slopes(
    monthly_rainfalls: list,
    *,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying rainfall linear regression slopes for each month passed through the dict.

    :param monthly_rainfalls: A list of instances of MonthlyRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall LinReg slopes for each month.
    """
    month_labels, slopes = [], []
    for monthly_rainfall in monthly_rainfalls:
        month_labels.append(monthly_rainfall.month.value)
        slopes.append(
            monthly_rainfall.get_linear_regression(
                begin_year=begin_year, end_year=end_year
            )[1]
        )

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x=month_labels,
            y=slopes,
            name="Monthly",
        )
    )

    figure.update_layout(
        title=f"{Label.LINEAR_REGRESSION.value} slope (mm/year) between {begin_year} and {end_year}"
    )
    figure.update_xaxes(title_text="Month")
    figure.update_yaxes(title_text=f"{Label.LINEAR_REGRESSION.value} slope (mm/year)")

    return figure


def get_bar_figure_of_seasonal_rainfall_linreg_slopes(
    seasonal_rainfalls: list,
    *,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying rainfall linear regression slopes for each season passed through the dict.

    :param seasonal_rainfalls: A list of instances of SeasonalRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall LinReg slopes for each season.
    """
    season_labels, slopes = [], []
    for seasonal_rainfall in seasonal_rainfalls:
        season_labels.append(seasonal_rainfall.season.value)
        slopes.append(
            seasonal_rainfall.get_linear_regression(
                begin_year=begin_year, end_year=end_year
            )[1]
        )

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x=season_labels,
            y=slopes,
            name="Seasonal",
        )
    )

    figure.update_layout(
        title=f"{Label.LINEAR_REGRESSION.value} slope (mm/year) between {begin_year} and {end_year}"
    )
    figure.update_xaxes(title_text="Season")
    figure.update_yaxes(title_text=f"{Label.LINEAR_REGRESSION.value} slope (mm/year)")

    return figure


def bar_monthly_relative_distances_to_normal(
    monthly_rainfalls: list,
    normal_year: int,
    begin_year: int,
    end_year: int,
) -> list[float | None]:
    """
    Plots a bar graphic displaying relative distances to normal for each month passed through the dict.

    :param monthly_rainfalls: A list of instances of MonthlyRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param normal_year: An integer representing the year
    to start computing the 30 years normal of the rainfall.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A list of the relative distances to normal (%) for each month.
    """
    month_labels, relative_distances_to_normal = [], []
    for monthly_rainfall in monthly_rainfalls:
        month_labels.append(monthly_rainfall.month.value[:3])
        relative_distances_to_normal.append(
            monthly_rainfall.get_relative_distance_to_normal(
                normal_year, begin_year, end_year
            )
        )

    bar_plot = plt.bar(
        month_labels,
        relative_distances_to_normal,
        label=f"Relative distance to {normal_year}-{normal_year + 29} normal between {begin_year} and {end_year} (%)",
    )
    plt.bar_label(bar_plot)
    plt.legend()

    return relative_distances_to_normal


def bar_seasonal_relative_distances_to_normal(
    seasonal_rainfalls: list,
    normal_year: int,
    begin_year: int,
    end_year: int,
) -> list[float | None]:
    """
    Plots a bar graphic displaying relative distances to normal for each season passed through the dict.

    :param seasonal_rainfalls: A list of instances of SeasonalRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param normal_year: An integer representing the year
    to start computing the 30 years normal of the rainfall.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A list of the relative distances to normal (%) for each season.
    """
    season_labels, relative_distances_to_normal = [], []
    for seasonal_rainfall in seasonal_rainfalls:
        season_labels.append(seasonal_rainfall.season.value)
        relative_distances_to_normal.append(
            seasonal_rainfall.get_relative_distance_to_normal(
                normal_year, begin_year, end_year
            )
        )

    bar_plot = plt.bar(
        season_labels,
        relative_distances_to_normal,
        label=f"Relative distance to {normal_year}-{normal_year + 29} normal between {begin_year} and {end_year} (%)",
    )
    plt.bar_label(bar_plot)
    plt.legend()

    return relative_distances_to_normal
