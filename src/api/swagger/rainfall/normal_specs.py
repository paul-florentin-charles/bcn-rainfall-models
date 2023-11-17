# pylint: disable=duplicate-code

"""
/rainfall/normal

Retrieve 30 years rainfall average for Barcelona after a given year.
Commonly called rainfall normal.
"""

import src.api.swagger.parameters_specs as param
from src.api.schemas import RainfallSchema

route_specs: dict = {
    "operationId": "getRainfallNormal",
    "summary": "Retrieve 30 years rainfall average for Barcelona after a given year.",
    "description": "Commonly called rainfall normal",
    "tags": [
        "rainfall"
    ],
    "responses": {
        "200": {
            "description": "The 30 years normal (in mm)",
            "schema": RainfallSchema
        }
    },
    "parameters": [
        param.begin_year,
        param.time_mode,
        param.month,
        param.season
    ],
    "produces": [
        "application/json"
    ]
}
