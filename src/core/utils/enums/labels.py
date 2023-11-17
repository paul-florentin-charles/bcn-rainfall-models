"""
Provides labels for retrieving interesting data within Pandas DataFrame.
"""

from src.core.utils.enums.base_enum import BaseEnum


class Label(str, BaseEnum):
    """
    An Enum listing labels in DataFrame columns.
    """
    YEAR: str = 'Year'
    RAINFALL: str = 'Rainfall'
    PERCENTAGE_OF_NORMAL: str = 'Percentage of normal'
    LINEAR_REGRESSION: str = 'Linear regression'
    SAVITZKY_GOLAY_FILTER: str = 'Savitzky–Golay filter'
    KMEANS: str = 'K-Means'
