"""
Provides functions to compute interesting and reusable generic metrics
over DataFrame containing rainfall data over years.
"""

from typing import Callable, Optional

import pandas as pd

from src.enums.labels import Label


def get_average_rainfall(yearly_rainfall: pd.DataFrame,
                         round_precision: Optional[int] = 2) -> float:
    """
    Computes Rainfall average for a specific year range.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param round_precision: A float representing the rainfall precision (optional).
    :return: A float representing the average Rainfall.
    """

    nb_years: int = len(yearly_rainfall)
    if nb_years == 0:
        return 0.

    year_rain = yearly_rainfall.sum(axis='rows')

    return round(year_rain.loc[Label.RAINFALL.value] / nb_years, round_precision)


def get_years_compared_to_given_rainfall_value(yearly_rainfall: pd.DataFrame,
                                               rainfall_value: float,
                                               comparator: Callable) -> int:
    """
    Computes the number of years that pass comparison to the given rainfall value
    for a specific year range.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param rainfall_value: A float representing the rainfall value.
    :param comparator: A comparator function that takes exactly two parameters.
    :return: The number of years compared to the given rainfall value as an integer.
    """
    yearly_rainfall = yearly_rainfall[
        comparator(yearly_rainfall[Label.RAINFALL.value], rainfall_value)
    ]

    return int(yearly_rainfall.count()[Label.YEAR.value])
