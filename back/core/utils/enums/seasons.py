"""
Provides list of Month (Enum) equivalents for all four seasons of the year.
"""

from back.core.utils.enums import BaseEnum
from back.core.utils.enums.months import Month


class Season(BaseEnum):
    """
    An Enum listing all seasons: 'winter', 'spring', 'summer', 'fall'.
    """

    WINTER = "winter"
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"

    def get_months(self):
        return MONTHS_BY_SEASON[self]


MONTHS_BY_SEASON: dict[Season, list[Month]] = {
    Season.WINTER: [Month.DECEMBER, Month.JANUARY, Month.FEBRUARY],
    Season.SPRING: [Month.MARCH, Month.APRIL, Month.MAY],
    Season.SUMMER: [Month.JUNE, Month.JULY, Month.AUGUST],
    Season.FALL: [Month.SEPTEMBER, Month.OCTOBER, Month.NOVEMBER],
}
