from _pytest.python_api import raises
from fastapi import HTTPException

from back.api import utils
from back.rainfall.utils import Month, Season, TimeMode


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
