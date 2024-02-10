"""
/graph/monthly_averages

Retrieve monthly averages of data as an SVG.
"""

import src.api.swagger.parameters_specs as param
from src.api.swagger.media_types import MediaType

route_specs: dict = {
    "operationId": "getMonthlyAverages",
    "summary": "Retrieve monthly averages of data as an SVG.",
    "tags": ["Graph"],
    "responses": {
        "200": {
            "description": "Monthly averages as an SVG",
            "content": MediaType.IMG_SVG,
        },
    },
    "parameters": [
        param.file_name,
        param.begin_year,
        param.end_year,
    ],
    "produces": MediaType.IMG_SVG,
}
