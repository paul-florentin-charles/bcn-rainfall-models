# pylint: disable=duplicate-code

"""
/rainfall/average

Retrieve average rainfall for Barcelona between two years.
Only the starting year is compulsory.
If no ending year is precised, computes average until most recent year available.
"""

import src.api.swagger.parameters_specs as param
from src.api.schemas import AverageYearlyRainfall

route_specs: dict = {
    "operationId": "getRainfallAverage",
    "summary": "Retrieve average rainfall for Barcelona between two years.",
    "description": "Only the starting year is compulsory.\n"
                   "If no ending year is precised, "
                   "computes average until most recent year available.",
    "tags": [
        "rainfall"
    ],
    "responses": {
        "200": {
            "description": "The average rainfall (in mm)",
            "schema": AverageYearlyRainfall
        }
    },
    "parameters": [
        param.begin_year,
        param.end_year
    ],
    "produces": [
        "application/json"
    ]
}
