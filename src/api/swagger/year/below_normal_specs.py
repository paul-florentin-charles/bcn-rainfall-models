# pylint: disable=duplicate-code

"""
/year/below_normal

Computes the number of years below normal for a specific year range.
Normal is computed as a 30 years average starting from the year set via normal_year.
"""

import src.api.swagger.parameters_specs as param


route_specs: dict = {
    "operationId": "getYearsBelowNormal",
    "summary": "Computes the number of years below normal for a specific year range.",
    "description": "Normal is computed as a 30 years average "
                   "starting from the year set via normal_year.",
    "tags": [
        "year"
    ],
    "responses": {
        "200": {
            "description": "the number of years below normal",
            "schema": {
                "type": "integer",
                "example": 27
            }
        }
    },
    "parameters": [
        param.normal_year,
        param.begin_year,
        param.end_year
    ],
    "produces": [
        "application/json"
    ]
}
