"""
/rainfall/standard_deviation

Compute the standard deviation of rainfall for Barcelona between two years.
Only the starting year is compulsory.
If no ending year is precised, computes average until most recent year available.
"""

import src.api.swagger.parameters_specs as param
import src.api.swagger.error_specs as error
from src.api.schemas import RainfallSchema
from src.api.swagger.media_types import MediaType

route_specs: dict = {
    "operationId": "getRainfallStandardDeviation",
    "summary": "Compute the standard deviation of rainfall for Barcelona between two years.",
    "description": "Only the starting year is compulsory.\n"
    "If no ending year is precised, "
    "computes average until most recent year available.",
    "tags": ["Rainfall"],
    "responses": {
        "200": {
            "description": "The rainfall standard deviation (in mm)",
            "schema": RainfallSchema,
        },
        "400": error.bad_request_specs,
    },
    "parameters": [param.begin_year, param.end_year, *param.time_params],
    "produces": MediaType.APP_JSON,
}
