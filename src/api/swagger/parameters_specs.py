"""
Swagger specifications for route parameters.
"""
from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode

normal_year: dict = {
    "default": 1971,
    "required": True,
    "type": "integer",
    "name": "normal_year",
    "in": "query",
}

begin_year: dict = {
    "default": 1991,
    "required": True,
    "type": "integer",
    "name": "begin_year",
    "in": "query",
}

end_year: dict = {
    "default": None,
    "required": False,
    "type": "integer",
    "name": "end_year",
    "in": "query",
}

time_mode: dict = {
    "default": TimeMode.YEARLY.name,
    "required": True,
    "type": "string",
    "enum": TimeMode.names(),
    "name": "time_mode",
    "in": "query",
}

month: dict = {
    "default": None,
    "required": False,
    "type": "string",
    "enum": Month.names(),
    "name": "month",
    "in": "query",
}

season: dict = {
    "default": None,
    "required": False,
    "type": "string",
    "enum": Season.names(),
    "name": "season",
    "in": "query",
}

time_params: tuple = (time_mode, month, season)

file_name: dict = {
    "default": None,
    "required": True,
    "type": "string",
    "name": "file_name",
    "description": "Name of the file to be retrieved",
    "in": "query",
}
