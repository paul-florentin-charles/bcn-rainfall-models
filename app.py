#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI app run with Uvicorn.
"""

import io

import matplotlib.pyplot as plt
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import StreamingResponse

from src.api.media_types import MediaType
from src.api.models import RainfallModel, RainfallWithNormalModel, YearWithNormalModel
from src.api.utils import (
    raise_time_mode_error_or_do_nothing,
)
from src.core.models.all_rainfall import AllRainfall
from src.core.utils.enums.labels import Label
from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode

all_rainfall = AllRainfall.from_config()

app = FastAPI(
    debug=True,
    root_path="/api",
    title="Barcelona Rainfall API",
    summary="An API that provides rainfall-related data of the city of Barcelona.",
    description=f"Available data is between {all_rainfall.starting_year} and {all_rainfall.get_last_year()}.",
)


@app.get(
    "/rainfall/average",
    summary="Retrieve rainfall average for Barcelona between two years.",
    description=f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}",
    tags=["Rainfall"],
    operation_id="getRainfallAverage",
)
async def get_rainfall_average(
    time_mode: TimeMode,
    begin_year: int,
    end_year: int | None = None,
    month: Month | None = None,
    season: Season | None = None,
) -> RainfallModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return RainfallModel(
        name="rainfall average (mm)",
        value=all_rainfall.get_average_rainfall(
            time_mode,
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
    month: Month | None = None,
    season: Season | None = None,
) -> RainfallModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
        name="rainfall normal (mm)",
        value=all_rainfall.get_normal(
            time_mode,
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
    "Its formula is `(average - normal) / normal * 100` <br> "
    "1. `average` is average rainfall computed between `begin_year` and `end_year`<br>"
    "2. `normal` is normal rainfall computed from `normal_year`<br>"
    "If 100%, average is twice the normal. <br>"
    "If -50%, average is half the normal. <br>"
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Rainfall"],
    operation_id="getRainfallRelativeDistanceToNormal",
)
async def get_rainfall_relative_distance_to_normal(
    time_mode: TimeMode,
    begin_year: int,
    normal_year: int,
    end_year: int | None = None,
    month: Month | None = None,
    season: Season | None = None,
) -> RainfallWithNormalModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return RainfallWithNormalModel(
        name="relative distance to rainfall normal (%)",
        value=all_rainfall.get_relative_distance_to_normal(
            time_mode,
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
    description=f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Rainfall"],
    operation_id="getRainfallStandardDeviation",
)
async def get_rainfall_standard_deviation(
    time_mode: TimeMode,
    begin_year: int,
    end_year: int | None = None,
    month: Month | None = None,
    season: Season | None = None,
    weigh_by_average: bool = False,
) -> RainfallModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return RainfallModel(
        name=f"rainfall standard deviation {"weighted by average" if weigh_by_average else "(mm)"}",
        value=all_rainfall.get_rainfall_standard_deviation(
            time_mode,
            begin_year=begin_year,
            end_year=end_year,
            month=month.value if month else None,
            season=season.value if season else None,
            weigh_by_average=weigh_by_average,
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
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Year"],
    operation_id="getYearsBelowNormal",
)
async def get_years_below_normal(
    time_mode: TimeMode,
    begin_year: int,
    normal_year: int,
    end_year: int | None = None,
    month: Month | None = None,
    season: Season | None = None,
) -> YearWithNormalModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return YearWithNormalModel(
        name="years below rainfall normal",
        value=all_rainfall.get_years_below_normal(
            time_mode,
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
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Year"],
    operation_id="getYearsAboveNormal",
)
async def get_years_above_normal(
    time_mode: TimeMode,
    begin_year: int,
    normal_year: int,
    end_year: int | None = None,
    month: Month | None = None,
    season: Season | None = None,
) -> YearWithNormalModel:
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    return YearWithNormalModel(
        name="years above rainfall normal",
        value=all_rainfall.get_years_above_normal(
            time_mode,
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
    description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["CSV"],
    operation_id="getMinimalCsv",
)
def get_minimal_csv(
    time_mode: TimeMode,
    begin_year: int,
    end_year: int | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    month_value: str = month.value if time_mode == TimeMode.MONTHLY else None  # type: ignore
    season_value: str = season.value if time_mode == TimeMode.SEASONAL else None  # type: ignore

    csv_str = (
        all_rainfall.export_as_csv(
            time_mode,
            begin_year=begin_year,
            end_year=end_year,
            month=month_value,
            season=season_value,
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
    "/graph/rainfall_by_year",
    response_class=StreamingResponse,
    summary="Retrieve rainfall by year as a PNG.",
    description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Graph"],
    operation_id="getRainfallByYear",
)
def get_rainfall_by_year(
    time_mode: TimeMode,
    begin_year: int,
    end_year: int | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    end_year = end_year or all_rainfall.get_last_year()

    success = all_rainfall.plot_rainfall_by_year(
        time_mode,
        begin_year=begin_year,
        end_year=end_year,
        month=month.value if month else None,
        season=season.value if season else None,
    )
    if success is False:
        raise HTTPException(
            status_code=400,
            detail=f"Data has not been successfully plotted, "
            f"check if your data has both '{Label.RAINFALL.value}' and '{Label.YEAR.value}' columns",
        )

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)

    filename = f"rainfall_by_year_{begin_year}_{end_year}.png"
    if time_mode == TimeMode.MONTHLY:
        filename = f"{month.value.lower()}_{filename}"  # type: ignore
    elif time_mode == TimeMode.SEASONAL:
        filename = f"{season.value}_{filename}"  # type: ignore

    return StreamingResponse(
        img_buffer,
        headers={"Content-Disposition": f"inline; filename={filename}"},
        media_type=MediaType.IMG_PNG.value,
    )


@app.get(
    "/graph/rainfall_averages",
    response_class=StreamingResponse,
    summary="Retrieve rainfall monthly or seasonal averages of data as a PNG.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Graph"],
    operation_id="getRainfallAverages",
)
def get_rainfall_averages(
    time_mode: TimeMode,
    begin_year: int,
    end_year: int | None = None,
):
    end_year = end_year or all_rainfall.get_last_year()

    averages = all_rainfall.bar_rainfall_averages(
        time_mode=time_mode, begin_year=begin_year, end_year=end_year
    )
    if averages is None:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)

    return StreamingResponse(
        img_buffer,
        headers={
            "Content-Disposition": f'inline; filename="rainfall_{time_mode.value}_averages_{begin_year}_{end_year}.png"'
        },
        media_type=MediaType.IMG_PNG.value,
    )


@app.get(
    "/graph/rainfall_linreg_slopes",
    response_class=StreamingResponse,
    summary="Retrieve rainfall monthly or seasonal linear regression slopes of data as a PNG.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Graph"],
    operation_id="getRainfallLinregSlopes",
)
def get_rainfall_linreg_slopes(
    time_mode: TimeMode,
    begin_year: int,
    end_year: int | None = None,
):
    end_year = end_year or all_rainfall.get_last_year()

    linreg_slopes = all_rainfall.bar_rainfall_linreg_slopes(
        time_mode=time_mode, begin_year=begin_year, end_year=end_year
    )
    if linreg_slopes is None:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)

    filename = f"rainfall_{time_mode.value}_linreg_slopes_{begin_year}_{end_year}.png"

    return StreamingResponse(
        img_buffer,
        headers={"Content-Disposition": f'inline; filename="{filename}"'},
        media_type=MediaType.IMG_PNG.value,
    )


@app.get(
    "/graph/relative_distances_to_normal",
    response_class=StreamingResponse,
    summary="Retrieve monthly or seasonal relative distances to normal (%) of data as a PNG.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {all_rainfall.get_last_year()}.",
    tags=["Graph"],
    operation_id="geRelativeDistancesToNormal",
)
def get_relative_distances_to_normal(
    time_mode: TimeMode,
    normal_year: int,
    begin_year: int,
    end_year: int | None = None,
):
    end_year = end_year or all_rainfall.get_last_year()

    relative_distances_to_normal = all_rainfall.bar_relative_distance_from_normal(
        time_mode=time_mode,
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
    )
    if relative_distances_to_normal is None:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    img_buffer.seek(0)

    filename = f"{time_mode.value}_relative_distances_to_{normal_year}_normal_{begin_year}_{end_year}.png"

    return StreamingResponse(
        img_buffer,
        headers={"Content-Disposition": f'inline; filename="{filename}"'},
        media_type=MediaType.IMG_PNG.value,
    )


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, log_level="debug")
