from src.core.utils.enums.months import Month


class TestMonths:
    @staticmethod
    def test_months_count():
        assert len(Month) == 12

    @staticmethod
    def test_january():
        month = Month.JANUARY

        assert isinstance(month.value, str)
        assert month.value == "January"

    @staticmethod
    def test_february():
        month = Month.FEBRUARY

        assert isinstance(month.value, str)
        assert month.value == "February"

    @staticmethod
    def test_march():
        month = Month.MARCH

        assert isinstance(month.value, str)
        assert month.value == "March"

    @staticmethod
    def test_april():
        month = Month.APRIL

        assert isinstance(month.value, str)
        assert month.value == "April"

    @staticmethod
    def test_may():
        month = Month.MAY

        assert isinstance(month.value, str)
        assert month.value == "May"

    @staticmethod
    def test_june():
        month = Month.JUNE

        assert isinstance(month.value, str)
        assert month.value == "June"

    @staticmethod
    def test_july():
        month = Month.JULY

        assert isinstance(month.value, str)
        assert month.value == "July"

    @staticmethod
    def test_august():
        month = Month.AUGUST

        assert isinstance(month.value, str)
        assert month.value == "August"

    @staticmethod
    def test_september():
        month = Month.SEPTEMBER

        assert isinstance(month.value, str)
        assert month.value == "September"

    @staticmethod
    def test_october():
        month = Month.OCTOBER

        assert isinstance(month.value, str)
        assert month.value == "October"

    @staticmethod
    def test_november():
        month = Month.NOVEMBER

        assert isinstance(month.value, str)
        assert month.value == "November"

    @staticmethod
    def test_december():
        month = Month.DECEMBER

        assert isinstance(month.value, str)
        assert month.value == "December"
