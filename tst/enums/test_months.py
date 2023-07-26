# pylint: disable=missing-docstring

from src.enums.months import Month


def test_months() -> None:
    assert len(Month) == 12

    month: Month = Month.MAY
    assert month.value == 5
