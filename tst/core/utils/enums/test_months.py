from src.core.utils.enums.months import Month


class TestMonths:
    @staticmethod
    def test_months_count():
        assert len(Month) == 12

    @staticmethod
    def test_january():
        month = Month.JANUARY

        assert isinstance(month.value, int)
        assert month.value == 1

    @staticmethod
    def test_february():
        month = Month.FEBRUARY

        assert isinstance(month.value, int)
        assert month.value == 2

    @staticmethod
    def test_march():
        month = Month.MARCH

        assert isinstance(month.value, int)
        assert month.value == 3

    @staticmethod
    def test_april():
        month = Month.APRIL

        assert isinstance(month.value, int)
        assert month.value == 4

    @staticmethod
    def test_may():
        month = Month.MAY

        assert isinstance(month.value, int)
        assert month.value == 5

    @staticmethod
    def test_june():
        month = Month.JUNE

        assert isinstance(month.value, int)
        assert month.value == 6

    @staticmethod
    def test_july():
        month = Month.JULY

        assert isinstance(month.value, int)
        assert month.value == 7

    @staticmethod
    def test_august():
        month = Month.AUGUST

        assert isinstance(month.value, int)
        assert month.value == 8

    @staticmethod
    def test_september():
        month = Month.SEPTEMBER

        assert isinstance(month.value, int)
        assert month.value == 9

    @staticmethod
    def test_october():
        month = Month.OCTOBER

        assert isinstance(month.value, int)
        assert month.value == 10

    @staticmethod
    def test_november():
        month = Month.NOVEMBER

        assert isinstance(month.value, int)
        assert month.value == 11

    @staticmethod
    def test_december():
        month = Month.DECEMBER

        assert isinstance(month.value, int)
        assert month.value == 12
