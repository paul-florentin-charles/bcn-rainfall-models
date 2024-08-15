"""
Swagger specifications for route parameters.
"""
from typing import Any

from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode

normal_year: dict[str, Any] = {
    "default": 1971,
    "required": True,
    "type": "integer",
    "name": "normal_year",
    "in": "query",
}

begin_year: dict[str, Any] = {
    "default": 1991,
    "required": True,
    "type": "integer",
    "name": "begin_year",
    "in": "query",
}

end_year: dict[str, Any] = {
    "default": None,
    "required": False,
    "type": "integer",
    "name": "end_year",
    "in": "query",
}

time_mode: dict[str, Any] = {
    "default": TimeMode.YEARLY.value,
    "required": True,
    "type": "string",
    "enum": TimeMode.values(),
    "name": "time_mode",
    "in": "query",
}

month: dict[str, Any] = {
    "default": None,
    "required": False,
    "type": "string",
    "enum": Month.values(),
    "name": "month",
    "in": "query",
}

season: dict[str, Any] = {
    "default": None,
    "required": False,
    "type": "string",
    "enum": Season.values(),
    "name": "season",
    "in": "query",
}

time_params = (time_mode, month, season)

file_name: dict[str, Any] = {
    "default": None,
    "required": True,
    "type": "string",
    "name": "file_name",
    "description": "Name of the file to be retrieved",
    "in": "query",
}
