from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode


class BaseRainfallModel(BaseModel):
    """
    Base model for depicting a value linked to rainfall data.
    It could be either a float value for rainfall or an integer value for years.
    Should be used as a parent class.
    """

    name: str
    value: float | int
    begin_year: int
    end_year: int | None = None
    time_mode: TimeMode = TimeMode.YEARLY
    month: Optional[Month] = None
    season: Optional[Season] = None


class RainfallModel(BaseRainfallModel):
    """
    Model for depicting a float value in mm (rainfall value).
    """

    value: float


class RainfallWithNormalModel(RainfallModel):
    """
    Model for depicting a float value in mm (rainfall value) along with a year to start computing normal from.
    """

    normal_year: int


class YearWithNormalModel(BaseRainfallModel):
    """
    Model for depicting an integer value (year count) along with a year to start computing normal from.
    """

    value: int
    normal_year: int
