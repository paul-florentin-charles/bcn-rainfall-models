from back.core.utils.enums.seasons import Season


class TestSeasons:
    @staticmethod
    def test_seasons_count():
        assert len(Season) == 4

    @staticmethod
    def test_winter():
        season = Season.WINTER

        assert isinstance(season.value, str)
        assert season.value == "winter"

    @staticmethod
    def test_spring():
        season = Season.SPRING

        assert isinstance(season.value, str)
        assert season.value == "spring"

    @staticmethod
    def test_summer():
        season = Season.SUMMER

        assert isinstance(season.value, str)
        assert season.value == "summer"

    @staticmethod
    def test_fall():
        season = Season.FALL

        assert isinstance(season.value, str)
        assert season.value == "fall"
