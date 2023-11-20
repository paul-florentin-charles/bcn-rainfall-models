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
    "in": "query"
}

begin_year: dict = {
    "default": 1991,
    "required": True,
    "type": "integer",
    "name": "begin_year",
    "in": "query"
}

end_year: dict = {
    "default": None,
    "required": False,
    "type": "integer",
    "name": "end_year",
    "in": "query"
}

time_mode: dict = {
    "default": TimeMode.YEARLY.value,
    "required": False,
    "type": "string",
    "enum": TimeMode.values(),
    "name": "time_mode",
    "in": "query"
}

month: dict = {
    "default": None,
    "required": False,
    "type": "string",
    "enum": Month.names(),
    "name": "month",
    "in": "query"
}

season: dict = {
    "default": None,
    "required": False,
    "type": "string",
    "enum": Season.names(),
    "name": "season",
    "in": "query"
}

csv_path: dict = {
    "default": "data.csv",
    "required": True,
    "type": "string",
    "name": "csv_path",
    "in": "query"
}
