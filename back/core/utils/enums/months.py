"""
Provides integer equivalents for months.
"""

from back.core.utils.enums import BaseEnum


class Month(BaseEnum):
    """
    An Enum listing all months.
    """

    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"

    def get_rank(self) -> int:
        return MONTH_RANK_DICT[self]


MONTH_RANK_DICT: dict[Month, int] = {
    Month.JANUARY: 1,
    Month.FEBRUARY: 2,
    Month.MARCH: 3,
    Month.APRIL: 4,
    Month.MAY: 5,
    Month.JUNE: 6,
    Month.JULY: 7,
    Month.AUGUST: 8,
    Month.SEPTEMBER: 9,
    Month.OCTOBER: 10,
    Month.NOVEMBER: 11,
    Month.DECEMBER: 12,
}
