# pylint: disable=duplicate-code

"""
/rainfall/normal

Retrieve 30 years rainfall average for Barcelona after a given year.
Commonly called rainfall normal.
"""

import src.api.swagger.parameters_specs as param


route_specs: dict = {
    "operationId": "getRainfallNormal",
    "summary": "Retrieve 30 years rainfall average for Barcelona after a given year.",
    "description": "Commonly called rainfall normal",
    "tags": [
        "rainfall"
    ],
    "responses": {
        "200": {
            "description": "the 30 years normal (in mm)",
            "schema": {
                "type": "number",
                "example": 607.28
            }
        }
    },
    "parameters": [
        param.begin_year
    ],
    "produces": [
        "application/json"
    ]
}
