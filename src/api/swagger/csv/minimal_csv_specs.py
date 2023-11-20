# pylint: disable=duplicate-code

"""
/csv/minimal_csv

Retrieve minimal CSV of rainfall data [Year/Rainfall].
Could either be for rainfall upon a whole year, a specific month or a given season.
"""

import src.api.swagger.parameters_specs as param

route_specs: dict = {
    "operationId": "getMinimalCsv",
    "summary": "Retrieve minimal CSV of rainfall data [Year/Rainfall].",
    "description": "Could either be for rainfall upon a whole year, "
                   "a specific month or a given season.",
    "tags": [
        "CSV"
    ],
    "responses": {
        "200": {
            "description": "Rainfall data according the year as a CSV",
            "content": "text/csv"
        }
    },
    "parameters": [
        param.time_mode,
        param.month,
        param.season,
        param.csv_path
    ],
    "produces": [
        "text/csv"
    ]
}
