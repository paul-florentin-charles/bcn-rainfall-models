"""
/year/below_normal

Computes the number of years below normal for a specific year range.
Normal is computed as a 30 years average starting from the year set via normal_year.
"""

import src.api.swagger.parameters_specs as param
from src.api.schemas import YearsAboveOrBelowNormalSchema
from src.api.swagger.media_types import MediaType

route_specs: dict = {
    "operationId": "getYearsBelowNormal",
    "summary": "Computes the number of years below normal for a specific year range.",
    "description": "Normal is computed as a 30 years average "
    "starting from the year set via normal_year.",
    "tags": ["Year"],
    "responses": {
        "200": {
            "description": "The number of years below normal",
            "schema": YearsAboveOrBelowNormalSchema,
        }
    },
    "parameters": [
        param.normal_year,
        param.begin_year,
        param.end_year,
        *param.time_params,
    ],
    "produces": MediaType.APP_JSON,
}
