"""
/rainfall/normal

Retrieve 30 years rainfall average for Barcelona after a given year.
Commonly called rainfall normal.
"""

import src.api.swagger.parameters_specs as param
import src.api.swagger.error_specs as error
from src.api.schemas import RainfallSchema
from src.api.swagger.media_types import MediaType

route_specs: dict = {
    "operationId": "getRainfallNormal",
    "summary": "Retrieve 30 years rainfall average for Barcelona after a given year.",
    "description": "Commonly called rainfall normal",
    "tags": ["Rainfall"],
    "responses": {
        "200": {"description": "The 30 years normal (in mm)", "schema": RainfallSchema},
        "400": error.bad_request_specs,
    },
    "parameters": [param.begin_year, *param.time_params],
    "produces": MediaType.APP_JSON,
}
