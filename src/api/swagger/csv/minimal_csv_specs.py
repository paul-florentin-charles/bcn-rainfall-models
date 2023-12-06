"""
/csv/minimal_csv

Retrieve minimal CSV of rainfall data [Year/Rainfall].
Could either be for rainfall upon a whole year, a specific month or a given season.
"""

import src.api.swagger.parameters_specs as param
import src.api.swagger.error_specs as error
from src.api.swagger.media_types import MediaType

route_specs: dict = {
    "operationId": "getMinimalCsv",
    "summary": "Retrieve minimal CSV of rainfall data [Year/Rainfall].",
    "description": "Could either be for rainfall upon a whole year, "
    "a specific month or a given season.",
    "tags": ["CSV"],
    "responses": {
        "200": {
            "description": "Rainfall data according the year as a CSV",
            "content": MediaType.TXT_CSV,
        },
        "400": error.bad_request_specs,
    },
    "parameters": [param.file_name, *param.time_params],
    "produces": MediaType.TXT_CSV,
}
