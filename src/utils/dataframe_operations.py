"""
Provides functions to do operations on DataFrame objects
containing rainfall data over years.
"""

from typing import Optional

import pandas as pd

from src.enums.labels import Label


def get_rainfall_within_year_interval(yearly_rainfall: pd.DataFrame,
                                      begin_year: Optional[int] = None,
                                      end_year: Optional[int] = None) -> pd.DataFrame:
    """
    Retrieves Yearly Rainfall within a specific year range.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param begin_year: An integer representing the year
    to start getting our rainfall values (optional).
    :param end_year: An integer representing the year
    to end getting our rainfall values (optional).
    :return: A pandas DataFrame displaying rainfall data (in mm)
    according to year.
    """
    if begin_year is not None:
        yearly_rainfall = yearly_rainfall[yearly_rainfall[Label.YEAR.value] >= begin_year]

    if end_year is not None:
        yearly_rainfall = yearly_rainfall[yearly_rainfall[Label.YEAR.value] <= end_year]

    return yearly_rainfall
