from pydantic import BaseModel

from back.core.utils.enums.months import Month
from back.core.utils.enums.seasons import Season
from back.core.utils.enums.time_modes import TimeMode


class RainfallModel(BaseModel):
    """
    Model for depicting a value linked to rainfall data.
    It could be either a float value for rainfall or an integer value for years.
    """

    name: str
    value: float | int
    begin_year: int
    end_year: int | None = None
    normal_year: int | None = None
    time_mode: TimeMode = TimeMode.YEARLY
    month: Month | None = None
    season: Season | None = None
