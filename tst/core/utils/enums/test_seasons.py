from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season


class TestSeasons:
    @staticmethod
    def test_seasons_count():
        assert len(Season) == 4

    @staticmethod
    def test_winter():
        season = Season.WINTER

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)

    @staticmethod
    def test_spring():
        season = Season.SPRING

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)

    @staticmethod
    def test_summer():
        season = Season.SUMMER

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)

    @staticmethod
    def test_fall():
        season = Season.FALL

        assert isinstance(season.value, list)
        assert len(season.value) == 3
        for month in season.value:
            assert isinstance(month, Month)
