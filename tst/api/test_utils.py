from _pytest.python_api import raises
from fastapi import HTTPException

from src.api import utils
from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode


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
