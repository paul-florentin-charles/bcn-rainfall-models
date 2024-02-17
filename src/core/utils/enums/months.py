"""
Provides integer equivalents for months.
"""

from src.core.utils.enums.base_enum import BaseEnum


class Month(int, BaseEnum):
    """
    An Enum listing months as integers.
    """

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12
