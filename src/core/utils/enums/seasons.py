"""
Provides list of Month (Enum) equivalents for all four seasons of the year.
"""

from enum import Enum

from src.core.utils.enums.months import Month


class Season(list, Enum):
    """
    An enum listing seasons (winter, spring, summer and fall) as lists of Month (Enum).
    """
    WINTER: list = [Month.DECEMBER, Month.JANUARY, Month.FEBRUARY]
    SPRING: list = [Month.MARCH, Month.APRIL, Month.MAY]
    SUMMER: list = [Month.JUNE, Month.JULY, Month.AUGUST]
    FALL: list = [Month.SEPTEMBER, Month.OCTOBER, Month.NOVEMBER]
