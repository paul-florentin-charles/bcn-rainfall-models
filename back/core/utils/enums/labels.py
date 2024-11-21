"""
Provides labels for retrieving interesting data within Pandas DataFrame.
"""

from back.core.utils.enums.base_enum import BaseEnum


class Label(str, BaseEnum):
    """
    An Enum listing labels in DataFrame columns.
    """

    YEAR = "Year"
    RAINFALL = "Rainfall"
    PERCENTAGE_OF_NORMAL = "Percentage of normal"
    LINEAR_REGRESSION = "Linear regression"
    SAVITZKY_GOLAY_FILTER = "Savitzky–Golay filter"
    KMEANS = "K-Means"
