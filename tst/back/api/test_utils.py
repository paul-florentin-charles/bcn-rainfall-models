from _pytest.python_api import raises
from fastapi import HTTPException

from back.api import utils
from back.core.utils.enums.months import Month
from back.core.utils.enums.seasons import Season
from back.core.utils.enums.time_modes import TimeMode


def test_raise_time_mode_error_or_do_nothing():
    assert utils.raise_time_mode_error_or_do_nothing(TimeMode.YEARLY) is None

    assert (
        utils.raise_time_mode_error_or_do_nothing(TimeMode.MONTHLY, month=Month.MAY)
        is None
    )

    assert (
        utils.raise_time_mode_error_or_do_nothing(TimeMode.SEASONAL, season=Season.FALL)
        is None
    )

    with raises(HTTPException):
        utils.raise_time_mode_error_or_do_nothing(TimeMode.MONTHLY, month=None)

    with raises(HTTPException):
        utils.raise_time_mode_error_or_do_nothing(TimeMode.SEASONAL, season=None)


def test_raise_year_related_error_or_do_nothing():
    assert utils.raise_year_related_error_or_do_nothing(1975, 1995) is None

    with raises(HTTPException):
        utils.raise_year_related_error_or_do_nothing(1995, 1975)
