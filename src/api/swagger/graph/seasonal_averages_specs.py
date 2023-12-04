"""
/graph/seasonal_averages

Retrieve seasonal averages of data as an SVG.
"""

import src.api.swagger.parameters_specs as param
from src.api.swagger.media_types import MediaType

route_specs: dict = {
    "operationId": "getSeasonalAverages",
    "summary": "Retrieve seasonal averages of data as an SVG.",
    "tags": ["Graph"],
    "responses": {
        "200": {
            "description": "Seasonal averages as an SVG",
            "content": MediaType.IMG_SVG,
        },
    },
    "parameters": [param.svg_path],
    "produces": MediaType.IMG_SVG,
}
