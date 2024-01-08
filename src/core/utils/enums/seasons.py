"""
Provides list of Month (Enum) equivalents for all four seasons of the year.
"""
from typing import List

from src.core.utils.enums.base_enum import BaseEnum
from src.core.utils.enums.months import Month


class Season(BaseEnum):
    """
    An enum listing seasons (winter, spring, summer and fall) as lists of Month (Enum).
    """

    WINTER: List[Month] = [Month.DECEMBER, Month.JANUARY, Month.FEBRUARY]
    SPRING: List[Month] = [Month.MARCH, Month.APRIL, Month.MAY]
    SUMMER: List[Month] = [Month.JUNE, Month.JULY, Month.AUGUST]
    FALL: List[Month] = [Month.SEPTEMBER, Month.OCTOBER, Month.NOVEMBER]
