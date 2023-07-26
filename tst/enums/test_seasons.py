# pylint: disable=missing-docstring

from src.enums.months import Month
from src.enums.seasons import Season


def test_seasons() -> None:
    assert len(Season) == 4

    season: Season = Season.WINTER
    assert isinstance(season.value, list)
    assert len(season.value) == 3
    assert isinstance(season.value[0], Month)
