"""
Provides a bunch of Marshmallow Schemas to validate rainfall data processed through the API.
"""
from http import HTTPStatus
from typing import Optional, Union

from flasgger import Schema, fields

from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode
import src.api.swagger.parameters_specs as param


class BaseSchema(Schema):
    """
    Base schema for depicting a value linked to rainfall data.
    It could be either float values or integer values (rainfall/years).
    Should be used as a parent class.
    """

    name: str = fields.Str()
    value: Union[float, int] = fields.Number()
    begin_year: int = fields.Int(load_default=param.begin_year["default"])
    end_year: Optional[int] = fields.Int(allow_none=True)
    time_mode: TimeMode = fields.Enum(TimeMode, load_default=TimeMode.YEARLY)
    month: Optional[Month] = fields.Enum(Month, allow_none=True)
    season: Optional[Season] = fields.Enum(Season, allow_none=True)


class RainfallSchema(BaseSchema):
    """
    Schema for depicting a float value in mm (rainfall value).
    """

    value: float = fields.Float()


class RelativeDistanceToRainfallNormalSchema(RainfallSchema):
    """
    Schema for depicting a relative distance to rainfall normal.
    """

    normal_year: int = fields.Int(load_default=param.normal_year["default"])


class YearsAboveOrBelowNormalSchema(BaseSchema):
    """
    Schema for giving the number of years above or below rainfall normal.
    """

    normal_year: int = fields.Int(load_default=param.normal_year["default"])
    value: float = fields.Int()


class ApiError(Schema):
    """
    Generic schema to depict any error.
    """

    code: int = fields.Int(dump_default=HTTPStatus.BAD_REQUEST.value)
    name: str = fields.Str(dump_default=HTTPStatus.BAD_REQUEST.phrase)
    message: str = fields.Str()
