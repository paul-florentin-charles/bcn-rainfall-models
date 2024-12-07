"""
Provides useful functions for plotting rainfall data in all shapes.
"""

import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objs as go

from back.core.utils.enums import Label, TimeMode


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
            name=label.value,
        )
    )

    figure.update_layout(title=figure_label or label.value)
    figure.update_xaxes(title_text=Label.YEAR.value)
    figure.update_yaxes(title_text=label.value)

    return figure


def get_bar_figure_of_rainfall_averages(
    rainfall_instance_by_label: dict,
    *,
    time_mode: TimeMode,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying average rainfall for each month or for each season passed through the dict.

    :param rainfall_instance_by_label: A dict of months respectively mapped with instances of MonthlyRainfall
    or a dict of seasons respectively mapped with instances of SeasonalRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall averages for each month or for each season.
    """
    labels: list[str] = []
    averages: list[float] = []
    for label, rainfall_instance in rainfall_instance_by_label.items():
        labels.append(label)

        averages.append(
            rainfall_instance.get_average_yearly_rainfall(
                begin_year=begin_year, end_year=end_year
            )
        )

    figure = go.Figure()
    figure.add_trace(go.Bar(x=labels, y=averages, name=time_mode.value.capitalize()))

    figure.update_layout(
        title=f"Average rainfall (mm) between {begin_year} and {end_year}"
    )
    figure.update_xaxes(title_text=time_mode.value.capitalize()[:-2])
    figure.update_yaxes(title_text=Label.RAINFALL.value)

    return figure


def get_bar_figure_of_rainfall_linreg_slopes(
    rainfall_instance_by_label: dict,
    *,
    time_mode: TimeMode,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying rainfall linear regression slopes for each month or
    for each season passed through the dict.

    :param rainfall_instance_by_label: A dict of months respectively mapped with instances of MonthlyRainfall
    or a dict of seasons respectively mapped with instances of SeasonalRainfall.
    :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall LinReg slopes for each month.
    """
    labels: list[str] = []
    slopes: list[float] = []
    r2_scores: list[float] = []
    for label, rainfall_instance in rainfall_instance_by_label.items():
        labels.append(label)

        (r2_score, slope), _ = rainfall_instance.get_linear_regression(
            begin_year=begin_year, end_year=end_year
        )

        slopes.append(slope)
        r2_scores.append(r2_score)

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x=labels,
            y=slopes,
            name=time_mode.value.capitalize(),
        )
    )

    figure.update_layout(
        title=f"{Label.LINEAR_REGRESSION.value} slope (mm/year) between {begin_year} and {end_year}"
    )
    figure.update_xaxes(title_text=time_mode.value.capitalize()[:-2])
    figure.update_yaxes(title_text=f"{Label.LINEAR_REGRESSION.value} slope (mm/year)")

    return figure


def get_bar_figure_of_relative_distances_to_normal(
    rainfall_instance_by_label: dict,
    *,
    time_mode: TimeMode,
    normal_year: int,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying relative distances to normal for each month or
    for each season passed through the dict.

    :param rainfall_instance_by_label: A dict of months respectively mapped with instances of MonthlyRainfall
    or a dict of seasons respectively mapped with instances of SeasonalRainfall.
    :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
    :param normal_year: An integer representing the year
    to start computing the 30 years normal of the rainfall.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall relative distances to normal for each month or for each season.
    """
    labels: list[str] = []
    relative_distances_to_normal: list[float] = []
    for label, rainfall_instance in rainfall_instance_by_label.items():
        labels.append(label)
        relative_distances_to_normal.append(
            rainfall_instance.get_relative_distance_to_normal(
                normal_year=normal_year, begin_year=begin_year, end_year=end_year
            )
        )

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x=labels,
            y=relative_distances_to_normal,
            name=time_mode.value.capitalize(),
        )
    )

    figure.update_layout(
        title=f"Relative distance to {normal_year}-{normal_year + 29} normal between {begin_year} and {end_year} (%)"
    )
    figure.update_xaxes(title_text=time_mode.value.capitalize()[:-2])
    figure.update_yaxes(
        title_text=f"Relative distance to {normal_year}-{normal_year + 29} normal"
    )

    return figure
