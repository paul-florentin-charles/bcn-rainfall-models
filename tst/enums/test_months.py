# pylint: disable=missing-docstring

from src.core.utils.enums.months import Month


class TestMonths:

    @staticmethod
    def test_months_count() -> None:
        assert len(Month) == 12

    @staticmethod
    def test_january() -> None:
        month: Month = Month.JANUARY

        assert isinstance(month.value, int)
        assert month.value == 1

    @staticmethod
    def test_february() -> None:
        month: Month = Month.FEBRUARY

        assert isinstance(month.value, int)
        assert month.value == 2

    @staticmethod
    def test_march() -> None:
        month: Month = Month.MARCH

        assert isinstance(month.value, int)
        assert month.value == 3

    @staticmethod
    def test_april() -> None:
        month: Month = Month.APRIL

        assert isinstance(month.value, int)
        assert month.value == 4

    @staticmethod
    def test_may() -> None:
        month: Month = Month.MAY

        assert isinstance(month.value, int)
        assert month.value == 5

    @staticmethod
    def test_june() -> None:
        month: Month = Month.JUNE

        assert isinstance(month.value, int)
        assert month.value == 6

    @staticmethod
    def test_july() -> None:
        month: Month = Month.JULY

        assert isinstance(month.value, int)
        assert month.value == 7

    @staticmethod
    def test_august() -> None:
        month: Month = Month.AUGUST

        assert isinstance(month.value, int)
        assert month.value == 8

    @staticmethod
    def test_september() -> None:
        month: Month = Month.SEPTEMBER

        assert isinstance(month.value, int)
        assert month.value == 9

    @staticmethod
    def test_october() -> None:
        month: Month = Month.OCTOBER

        assert isinstance(month.value, int)
        assert month.value == 10

    @staticmethod
    def test_november() -> None:
        month: Month = Month.NOVEMBER

        assert isinstance(month.value, int)
        assert month.value == 11

    @staticmethod
    def test_december() -> None:
        month: Month = Month.DECEMBER

        assert isinstance(month.value, int)
        assert month.value == 12
