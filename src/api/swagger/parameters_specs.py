"""
Swagger specifications for route parameters.
"""

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
    "default": 2020,
    "required": False,
    "type": "integer",
    "name": "end_year",
    "in": "query"
}
