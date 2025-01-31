"""
Module to provide a function that returns a dict linking FastAPI routes endpoints to their specifications.
"""

from typing import Any, Callable

from pydantic import BaseModel, Field
from starlette.responses import JSONResponse, StreamingResponse

from back.api.utils import RainfallModel
from back.rainfall.models import AllRainfall
from back.rainfall.utils import TimeMode

all_rainfall = AllRainfall.from_config()


MIN_YEAR_AVAILABLE = all_rainfall.starting_year
MAX_YEAR_AVAILABLE = all_rainfall.get_last_year()
MAX_NORMAL_YEAR_AVAILABLE = MAX_YEAR_AVAILABLE - 29

__all__ = [
    "all_rainfall",
    "get_endpoint_to_api_route_specs",
    "MIN_YEAR_AVAILABLE",
    "MAX_YEAR_AVAILABLE",
    "MAX_NORMAL_YEAR_AVAILABLE",
]


class APIRouteSpecs(BaseModel):
    path: str
    summary: str
    description: str | None = Field(default=None)
    response_model: Any = Field(default=None)
    tags: list[str] = Field(default_factory=list)
    response_class: Any = Field(default=JSONResponse)


def get_endpoint_to_api_route_specs() -> dict[Callable[..., Any], APIRouteSpecs]:
    from back.api.routes.csv import get_rainfall_by_year_as_csv
    from back.api.routes.graph import (
        get_rainfall_averages_as_plotly_json,
        get_rainfall_by_year_as_plotly_json,
        get_rainfall_linreg_slopes_as_plotly_json,
        get_relative_distances_to_normal_as_plotly_json,
    )
    from back.api.routes.rainfall import (
        get_rainfall_average,
        get_rainfall_normal,
        get_rainfall_relative_distance_to_normal,
        get_rainfall_standard_deviation,
    )
    from back.api.routes.year import get_years_above_normal, get_years_below_normal

    endpoint_to_rainfall_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_rainfall_average: APIRouteSpecs(
            path="/rainfall/average",
            summary="Retrieve rainfall average for Barcelona between two years.",
            description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_rainfall_normal: APIRouteSpecs(
            path="/rainfall/normal",
            summary="Retrieve 30 years rainfall average for Barcelona after a given year.",
            description="Commonly called rainfall normal.",
        ),
        get_rainfall_relative_distance_to_normal: APIRouteSpecs(
            path="/rainfall/relative_distance_to_normal",
            summary="Retrieve the rainfall relative distance to normal for Barcelona between two years.",
            description="The metric is a percentage that can be negative. <br>"
            "Its formula is `(average - normal) / normal * 100`. <br> "
            "1. `average` is average rainfall computed between `begin_year` and `end_year`<br>",
        ),
        get_rainfall_standard_deviation: APIRouteSpecs(
            path="/rainfall/standard_deviation",
            summary="Compute the standard deviation of rainfall for Barcelona between two years.",
            description=f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
    }

    for endpoint in endpoint_to_rainfall_api_route_specs.keys():
        endpoint_to_rainfall_api_route_specs[endpoint].response_model = RainfallModel
        endpoint_to_rainfall_api_route_specs[endpoint].tags = ["Rainfall"]

    endpoint_to_year_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_years_below_normal: APIRouteSpecs(
            path="/year/below_normal",
            summary="Compute the number of years below normal for a specific year range.",
            description="Normal is computed as a 30 years average "
            f"starting from the year set via normal_year. <br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_years_above_normal: APIRouteSpecs(
            path="/year/above_normal",
            summary="Compute the number of years above normal for a specific year range.",
            description="Normal is computed as a 30 years average "
            f"starting from the year set via normal_year. <br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
    }

    for endpoint in endpoint_to_year_api_route_specs.keys():
        endpoint_to_year_api_route_specs[endpoint].response_model = RainfallModel
        endpoint_to_year_api_route_specs[endpoint].tags = ["Year"]

    endpoint_to_graph_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_rainfall_by_year_as_plotly_json: APIRouteSpecs(
            path="/graph/rainfall_by_year",
            summary="Retrieve rainfall by year as a PNG or as a JSON.",
            description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_rainfall_averages_as_plotly_json: APIRouteSpecs(
            path="/graph/rainfall_averages",
            summary="Retrieve rainfall monthly or seasonal averages of data as a PNG or as a JSON.",
            description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_rainfall_linreg_slopes_as_plotly_json: APIRouteSpecs(
            path="/graph/rainfall_linreg_slopes",
            summary="Retrieve rainfall monthly or seasonal linear regression slopes of data as a PNG or as a JSON.",
            description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
        get_relative_distances_to_normal_as_plotly_json: APIRouteSpecs(
            path="/graph/relative_distances_to_normal",
            summary="Retrieve monthly or seasonal relative distances to normal (%) of data as a PNG or as a JSON.",
            description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
        ),
    }

    for endpoint in endpoint_to_graph_api_route_specs.keys():
        endpoint_to_graph_api_route_specs[endpoint].tags = ["Graph"]

    endpoint_to_csv_api_route_specs: dict[Callable[..., Any], APIRouteSpecs] = {
        get_rainfall_by_year_as_csv: APIRouteSpecs(
            path="/csv/rainfall_by_year",
            summary="Retrieve CSV of rainfall by year data: ['Year', 'Rainfall'] columns.",
            description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
            f"If no ending year is precised, most recent year available is taken: {MAX_YEAR_AVAILABLE}.",
            response_class=StreamingResponse,
            tags=["CSV"],
        ),
    }

    return {
        **endpoint_to_rainfall_api_route_specs,
        **endpoint_to_year_api_route_specs,
        **endpoint_to_graph_api_route_specs,
        **endpoint_to_csv_api_route_specs,
    }
