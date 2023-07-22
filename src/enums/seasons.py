from enum import Enum

from src.enums.months import Month


class Season(list, Enum):
    WINTER: list = [Month.DECEMBER, Month.JANUARY, Month.FEBRUARY]
    SPRING: list = [Month.MARCH, Month.APRIL, Month.MAY]
    SUMMER: list = [Month.JUNE, Month.JULY, Month.AUGUST]
    FALL: list = [Month.SEPTEMBER, Month.OCTOBER, Month.NOVEMBER]
