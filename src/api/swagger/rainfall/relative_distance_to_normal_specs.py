# pylint: disable=duplicate-code

"""
/rainfall/relative_distance_to_normal

Retrieve the rainfall relative distance to normal for Barcelona between two years.
The metric is a percentage that can be negative.
If 100%, all the years are above normal.
If -100%, all the years are below normal.
If 0%, there are as many years below as years above.
Only the starting year is compulsory.
If no ending year is precised, computes the relative distance until most recent year available.
"""

import src.api.swagger.parameters_specs as param
from src.api.schemas import RelativeDistanceToRainfallNormalSchema

route_specs: dict = {
    "operationId": "getRainfallRelativeDistanceToNormal",
    "summary": "Retrieve the rainfall relative distance to normal for Barcelona between two years.",
    "description": "The metric is a percentage that can be negative.\n "
                   "If 100%, all the years are above normal.\n"
                   "If -100%, all the years are below normal.\n"
                   "If 0%, there are as many years below as years above.\n"
                   "Only the starting year is compulsory.\n"
                   "If no ending year is precised, "
                   "computes the relative distance until most recent year available.",
    "tags": [
        "rainfall"
    ],
    "responses": {
        "200": {
            "description": "The relative distance to normal as a percentage.",
            "schema": RelativeDistanceToRainfallNormalSchema
        }
    },
    "parameters": [
        param.normal_year,
        param.begin_year,
        param.end_year,
        param.time_mode,
        param.month,
        param.season
    ],
    "produces": [
        "application/json"
    ]
}
