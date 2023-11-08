"""
Provides a bunch of Marshmallow Schemas to validate rainfall data processed through the API.
"""

from typing import Optional, Union

from flasgger import Schema, fields

from src.core.utils.enums.time_modes import TimeMode


class BaseRainfall(Schema):
    """
    Base schema for depicting a value linked to rainfall data.
    Should be used as a parent class.
    """
    value: Union[float, int] = fields.Number()
    begin_year: int = fields.Int()
    end_year: Optional[int] = fields.Int()
    time_mode: str = fields.Str()


class AverageYearlyRainfall(BaseRainfall):
    """
    Schema for depicting an average rainfall for a yearly time mode.
    """
    name: str = fields.Str(load_default='average rainfall')
    value: float = fields.Float()
    time_mode: str = fields.Str(load_default=TimeMode.YEARLY.value)


class NormalYearlyRainfall(BaseRainfall):
    """
    Schema for depicting a rainfall normal for a yearly time mode.
    """
    name: str = fields.Str(load_default='rainfall normal')
    value: float = fields.Float()
    time_mode: str = fields.Str(load_default=TimeMode.YEARLY.value)


class RelativeDistanceToNormalYearlyRainfall(BaseRainfall):
    """
    Schema for depicting a relative distance to rainfall normal for a yearly time mode.
    """
    name: str = fields.Str(load_default='rainfall relative distance to normal')
    value: float = fields.Float()
    time_mode: str = fields.Str(load_default=TimeMode.YEARLY.value)


class StandardDeviationYearlyRainfall(BaseRainfall):
    """
    Schema for depicting a rainfall standard deviation for a yearly time mode.
    """
    name: str = fields.Str(load_default='rainfall standard deviation')
    value: float = fields.Float()
    time_mode: str = fields.Str(load_default=TimeMode.YEARLY.value)


class YearsAboveNormalSchema(BaseRainfall):
    """
    Schema for giving the number of years above rainfall normal for a yearly time mode.
    """
    name: str = fields.Str(load_default='years above rainfall normal')
    value: float = fields.Int()
    time_mode: str = fields.Str(load_default=TimeMode.YEARLY.value)


class YearsBelowNormalSchema(BaseRainfall):
    """
    Schema for giving the number of years below rainfall normal for a yearly time mode.
    """
    name: str = fields.Str(load_default='years below rainfall normal')
    value: float = fields.Int()
    time_mode: str = fields.Str(load_default=TimeMode.YEARLY.value)
