# pylint: disable=missing-docstring

from core.utils.enums.months import Month
from core.utils.enums.seasons import Season


class TestSeasons:
    @staticmethod
    def test_seasons_count() -> None:
        assert len(Season) == 4

    @staticmethod
    def test_winter() -> None:
        season: Season = Season.WINTER

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)

    @staticmethod
    def test_spring() -> None:
        season: Season = Season.SPRING

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)

    @staticmethod
    def test_summer() -> None:
        season: Season = Season.SUMMER

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)

    @staticmethod
    def test_fall() -> None:
        season: Season = Season.FALL

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)
