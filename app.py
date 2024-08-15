#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI app run with Uvicorn.
"""
from __future__ import annotations

import io
from typing import Union

import matplotlib.pyplot as plt
import uvicorn
from fastapi import FastAPI
from starlette.responses import StreamingResponse

from src.api.media_types import MediaType
from src.api.models import RainfallModel, RainfallWithNormalModel, YearWithNormalModel
from src.api.utils import (
    raise_time_mode_error_or_do_nothing,
)
from src.core.models.all_rainfall import AllRainfall
from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode

all_rainfall = AllRainfall.from_config()

app = FastAPI(
    debug=True,
    root_path="/api",
    title="Barcelona Rainfall API",
    summary="An API that provides rainfall-related data of the city of Barcelona",
)


@app.get(
    "/rainfall/average",
    summary="Retrieve rainfall average for Barcelona between two years.",
    description=f"If no ending year is precised, "
    f"computes average until latest year available: {all_rainfall.get_last_year()}",
    tags=["Rainfall"],
    operation_id="getRainfallAverage",
)
async def get_rainfall_average(
    time_mode: TimeMode,
    begin_year: int,
    end_year: Union[int, None] = None,
    month: Union[Month, None] = None,
    season: Union[Season, None] = None,
) -> RainfallModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return RainfallModel(
        name="rainfall average (mm)",
        value=all_rainfall.get_average_rainfall(
            time_mode.value,
            begin_year=begin_year,
            end_year=end_year,
            month=month.value if month else None,
            season=season.value if season else None,
        ),  # type: ignore
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


@app.get(
    "/rainfall/normal",
    summary="Retrieve 30 years rainfall average for Barcelona after a given year.",
    description="Commonly called rainfall normal.",
    tags=["Rainfall"],
    operation_id="getRainfallNormal",
)
async def get_rainfall_normal(
    time_mode: TimeMode,
    begin_year: int,
    month: Union[Month, None] = None,
    season: Union[Season, None] = None,
) -> RainfallModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
        name="rainfall normal (mm)",
        value=all_rainfall.get_normal(
            time_mode.value,
            begin_year=begin_year,
            month=month.value if month else None,
            season=season.value if season else None,
        ),  # type: ignore
        begin_year=begin_year,
        end_year=begin_year + 29,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


@app.get(
    "/rainfall/relative_distance_to_normal",
    summary="Retrieve the rainfall relative distance to normal for Barcelona between two years.",
    description="The metric is a percentage that can be negative. <br>"
    "If 100%, all the years are above normal. <br>"
    "If -100%, all the years are below normal. <br>"
    "If 0%, there are as many years below as years above. <br>"
    "If no ending year is precised, "
    f"computes the relative distance until most recent year available: {all_rainfall.get_last_year()}.",
    tags=["Rainfall"],
    operation_id="getRainfallRelativeDistanceToNormal",
)
async def get_rainfall_relative_distance_to_normal(
    time_mode: TimeMode,
    begin_year: int,
    normal_year: int,
    end_year: Union[int, None] = None,
    month: Union[Month, None] = None,
    season: Union[Season, None] = None,
) -> RainfallWithNormalModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return RainfallWithNormalModel(
        name="relative distance to rainfall normal (%)",
        value=all_rainfall.get_relative_distance_from_normal(
            time_mode.value,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
            month=month.value if month else None,
            season=season.value if season else None,
        ),  # type: ignore
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


@app.get(
    "/rainfall/standard_deviation",
    summary="Compute the standard deviation of rainfall for Barcelona between two years.",
    description="If no ending year is precised, "
    f"computes the relative distance until most recent year available: {all_rainfall.get_last_year()}.",
    tags=["Rainfall"],
    operation_id="getRainfallStandardDeviation",
)
async def get_rainfall_standard_deviation(
    time_mode: TimeMode,
    begin_year: int,
    end_year: Union[int, None] = None,
    month: Union[Month, None] = None,
    season: Union[Season, None] = None,
) -> RainfallModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return RainfallModel(
        name="rainfall standard deviation (mm)",
        value=all_rainfall.get_rainfall_standard_deviation(
            time_mode.value,
            begin_year=begin_year,
            end_year=end_year,
            month=month.value if month else None,
            season=season.value if season else None,
        ),  # type: ignore
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


@app.get(
    "/year/below_normal",
    summary="Compute the number of years below normal for a specific year range.",
    description="Normal is computed as a 30 years average "
    "starting from the year set via normal_year. <br>"
    "If no ending year is precised, "
    f"computes the relative distance until most recent year available: {all_rainfall.get_last_year()}.",
    tags=["Year"],
    operation_id="getYearsBelowNormal",
)
async def get_years_below_normal(
    time_mode: TimeMode,
    begin_year: int,
    normal_year: int,
    end_year: Union[int, None] = None,
    month: Union[Month, None] = None,
    season: Union[Season, None] = None,
) -> YearWithNormalModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return YearWithNormalModel(
        name="years below rainfall normal",
        value=all_rainfall.get_years_below_normal(
            time_mode.value,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
            month=month.value if month else None,
            season=season.value if season else None,
        ),  # type: ignore
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


@app.get(
    "/year/above_normal",
    summary="Compute the number of years above normal for a specific year range.",
    description="Normal is computed as a 30 years average "
    "starting from the year set via normal_year. <br>"
    "If no ending year is precised, "
    f"computes the relative distance until most recent year available: {all_rainfall.get_last_year()}.",
    tags=["Year"],
    operation_id="getYearsAboveNormal",
)
async def get_years_above_normal(
    time_mode: TimeMode,
    begin_year: int,
    normal_year: int,
    end_year: Union[int, None] = None,
    month: Union[Month, None] = None,
    season: Union[Season, None] = None,
) -> YearWithNormalModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return YearWithNormalModel(
        name="years above rainfall normal",
        value=all_rainfall.get_years_above_normal(
            time_mode.value,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
            month=month.value if month else None,
            season=season.value if season else None,
        ),  # type: ignore
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


@app.get(
    "/csv/minimal_csv",
    response_class=StreamingResponse,
    summary="Retrieve minimal CSV of rainfall data [Year, Rainfall].",
    description="Could either be for rainfall upon a whole year, a specific month or a given season.",
    tags=["CSV"],
    operation_id="getMinimalCsv",
)
def get_minimal_csv(
    time_mode: TimeMode,
    month: Union[Month, None] = None,
    season: Union[Season, None] = None,
):
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    month_value: str = month.value if time_mode == TimeMode.MONTHLY else None  # type: ignore
    season_value: str = season.value if time_mode == TimeMode.SEASONAL else None  # type: ignore

    csv_str = (
        all_rainfall.export_as_csv(
            time_mode.value,
            month_value,
            season_value,
        )
        or ""
    )

    filename = f"rainfall_{all_rainfall.starting_year}_{all_rainfall.get_last_year()}"
    if month_value:
        filename += f"_{month_value.lower()}"
    elif season_value:
        filename += f"_{season_value}"

    return StreamingResponse(
        iter(csv_str),
        headers={"Content-Disposition": f'inline; filename="{filename}.csv"'},
        media_type=MediaType.TXT_CSV.value,
    )


@app.get(
    "/graph/rainfall_monthly_averages",
    response_class=StreamingResponse,
    summary="Retrieve rainfall monthly averages of data as a PNG.",
    description="If no ending year is precised, "
    f"computes the relative distance until most recent year available: {all_rainfall.get_last_year()}.",
    tags=["Graph"],
    operation_id="getRainfallMonthlyAverages",
)
def get_rainfall_monthly_averages(
    begin_year: int,
    end_year: Union[int, None] = None,
):
    end_year = end_year or all_rainfall.get_last_year()

    all_rainfall.bar_rainfall_averages(begin_year=begin_year, end_year=end_year)

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)

    return StreamingResponse(
        img_buffer,
        headers={
            "Content-Disposition": f'inline; filename="rainfall_monthly_averages_{begin_year}_{end_year}.png"'
        },
        media_type=MediaType.IMG_PNG.value,
    )


@app.get(
    "/graph/rainfall_seasonal_averages",
    response_class=StreamingResponse,
    summary="Retrieve rainfall seasonal averages of data as a PNG.",
    description="If no ending year is precised, "
    f"computes the relative distance until most recent year available: {all_rainfall.get_last_year()}.",
    tags=["Graph"],
    operation_id="getRainfallSeasonalAverages",
)
def get_rainfall_seasonal_averages(
    begin_year: int,
    end_year: Union[int, None] = None,
):
    end_year = end_year or all_rainfall.get_last_year()

    all_rainfall.bar_rainfall_averages(
        begin_year=begin_year, end_year=end_year, monthly=False
    )

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)

    return StreamingResponse(
        img_buffer,
        headers={
            "Content-Disposition": f'inline; filename="rainfall_seasonal_averages_{begin_year}_{end_year}.png"'
        },
        media_type=MediaType.IMG_PNG.value,
    )


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, log_level="debug")
