"""
Collection of utility functions for API purposes.
"""

from fastapi import HTTPException

from back.core.utils.enums.months import Month
from back.core.utils.enums.seasons import Season
from back.core.utils.enums.time_modes import TimeMode


def raise_time_mode_error_or_do_nothing(
    time_mode: TimeMode,
    month: Month | None = None,
    season: Season | None = None,
):
    """
    Manage errors related to time mode issues.

    :param time_mode: A TimeMode Enum ['yearly', 'monthly', 'seasonal']
    :param month: A Month Enum ['January', 'February', ..., 'December'].
    Set if time_mode is 'monthly' (optional).
    :param season: A Season Enum ['winter', 'spring', 'summer', 'fall'].
    Set if time_mode is 'seasonal' (optional).
    :raise HTTPException: if time_mode is 'monthly' and month is None or
    if time_mode is 'seasonal' and season is None.
    :return: None.
    """
    if time_mode == TimeMode.MONTHLY and month is None:
        raise HTTPException(status_code=400, detail="Month cannot be null.")

    if time_mode == TimeMode.SEASONAL and season is None:
        raise HTTPException(status_code=400, detail="Season cannot be null.")
