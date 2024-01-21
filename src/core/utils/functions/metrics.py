"""
Provides functions to compute interesting and reusable generic metrics
over DataFrame containing rainfall data over years.
"""
from __future__ import annotations

from typing import Callable

import pandas as pd

from src.core.utils.enums.labels import Label
from src.core.utils.functions import dataframe_operations as df_opr


def get_average_rainfall(
    yearly_rainfall: pd.DataFrame, round_precision: int | None = 2
) -> float:
    """
    Computes Rainfall average.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param round_precision: A float representing the rainfall precision (optional).
    :return: A float representing the average Rainfall.
    """
    nb_years: int = len(yearly_rainfall)
    if nb_years == 0:
        return 0.0

    return round(
        yearly_rainfall.sum(axis="rows").loc[Label.RAINFALL.value] / nb_years,  # type: ignore
        round_precision,
    )


def get_years_compared_to_given_rainfall_value(
    yearly_rainfall: pd.DataFrame, rainfall_value: float, comparator: Callable
) -> int:
    """
    Computes the number of years that conform specified comparison
    to the given rainfall value.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param rainfall_value: A float representing the rainfall value.
    :param comparator: A comparator function that takes exactly two parameters.
    :return: The number of years compared to the given rainfall value as an integer.
    """
    yearly_rainfall = yearly_rainfall[
        comparator(yearly_rainfall[Label.RAINFALL.value], rainfall_value)
    ]

    return int(yearly_rainfall.count()[Label.YEAR.value])


def get_clusters_number(yearly_rainfall: pd.DataFrame) -> int:
    """
    Computes the number of clusters.

    :param yearly_rainfall: A pandas DataFrame displaying clusters label according to year.
    :return: The number of clusters as an integer.
    """
    if Label.KMEANS not in yearly_rainfall.columns:
        return 0

    return max(yearly_rainfall[Label.KMEANS.value]) + 1


def get_normal(yearly_rainfall: pd.DataFrame, begin_year) -> float:
    """
    Computes average rainfall over 30 years time frame.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param begin_year: A year to start the time frame.
    :return: A float storing the normal.
    """

    return get_average_rainfall(
        df_opr.get_rainfall_within_year_interval(
            yearly_rainfall, begin_year, begin_year + 29
        )
    )
