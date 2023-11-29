"""
Provides integer equivalents for months.
"""

from src.core.utils.enums.base_enum import BaseEnum


class Month(int, BaseEnum):
    """
    An Enum listing months as integers.
    """

    JANUARY: int = 1
    FEBRUARY: int = 2
    MARCH: int = 3
    APRIL: int = 4
    MAY: int = 5
    JUNE: int = 6
    JULY: int = 7
    AUGUST: int = 8
    SEPTEMBER: int = 9
    OCTOBER: int = 10
    NOVEMBER: int = 11
    DECEMBER: int = 12
