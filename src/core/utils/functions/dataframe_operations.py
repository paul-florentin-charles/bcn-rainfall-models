"""
Provides functions to do operations on DataFrame objects
containing rainfall data over years.
"""

from typing import Optional

import pandas as pd

from core.utils.enums.labels import Label


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


def remove_column(yearly_rainfall: pd.DataFrame, label: Label) -> bool:
    """
    Remove a column from a DataFrame using its label.
    Removing 'Year' or 'Rainfall' columns is prevented.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data
    under various shapes according to year.
    :param label: A string corresponding to an existing column label.
    :return: A boolean set to whether the operation passed or not.
    """
    if label not in yearly_rainfall.columns.drop([Label.YEAR, Label.RAINFALL]):
        return False

    yearly_rainfall.pop(label.value)

    return True
