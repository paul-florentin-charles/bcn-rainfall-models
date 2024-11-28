"""
FastAPI client exposing API routes related to rainfall data of Barcelona.
"""

import io
from typing import Annotated

import matplotlib.pyplot as plt
from fastapi import FastAPI, HTTPException, Query
from starlette.responses import StreamingResponse

from back.api.media_types import MediaType
from back.api.models import RainfallModel
from back.api.utils import (
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)
from back.core.models import AllRainfall
from back.core.utils.enums.labels import Label
from back.core.utils.enums.months import Month
from back.core.utils.enums.seasons import Season
from back.core.utils.enums.time_modes import TimeMode

all_rainfall = AllRainfall.from_config()

min_year_available = all_rainfall.starting_year
max_year_available = all_rainfall.get_last_year()
max_normal_year_available = max_year_available - 29


app = FastAPI(
    debug=True,
    root_path="/api",
    title="Barcelona Rainfall API",
    summary="An API that provides rainfall-related data of the city of Barcelona.",
    description=f"Available data is between {min_year_available} and {max_year_available}.",
)


@app.get(
    "/rainfall/average",
    response_model=RainfallModel,
    summary="Retrieve rainfall average for Barcelona between two years.",
    description=f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Rainfall"],
    operation_id="getRainfallAverage",
)
async def get_rainfall_average(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
        name="rainfall average (mm)",
        value=all_rainfall.get_rainfall_average(
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
    response_model=RainfallModel,
    summary="Retrieve 30 years rainfall average for Barcelona after a given year.",
    description="Commonly called rainfall normal.",
    tags=["Rainfall"],
    operation_id="getRainfallNormal",
)
async def get_rainfall_normal(
    time_mode: TimeMode,
    begin_year: Annotated[
        int, Query(ge=min_year_available, le=max_normal_year_available)
    ],
    month: Month | None = None,
    season: Season | None = None,
):
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
    response_model=RainfallModel,
    summary="Retrieve the rainfall relative distance to normal for Barcelona between two years.",
    description="The metric is a percentage that can be negative. <br>"
    "Its formula is `(average - normal) / normal * 100`. <br> "
    "1. `average` is average rainfall computed between `begin_year` and `end_year`<br>"
    "2. `normal` is normal rainfall computed from `normal_year`<br>"
    "If 100%, average is twice the normal. <br>"
    "If -50%, average is half the normal. <br>"
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Rainfall"],
    operation_id="getRainfallRelativeDistanceToNormal",
)
async def get_rainfall_relative_distance_to_normal(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    normal_year: Annotated[
        int, Query(ge=min_year_available, le=max_normal_year_available)
    ],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
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
    response_model=RainfallModel,
    summary="Compute the standard deviation of rainfall for Barcelona between two years.",
    description=f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Rainfall"],
    operation_id="getRainfallStandardDeviation",
)
async def get_rainfall_standard_deviation(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
    weigh_by_average: bool = False,
):
    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

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
    response_model=RainfallModel,
    summary="Compute the number of years below normal for a specific year range.",
    description="Normal is computed as a 30 years average "
    "starting from the year set via normal_year. <br>"
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Year"],
    operation_id="getYearsBelowNormal",
)
async def get_years_below_normal(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    normal_year: Annotated[
        int, Query(ge=min_year_available, le=max_normal_year_available)
    ],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
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
    response_model=RainfallModel,
    summary="Compute the number of years above normal for a specific year range.",
    description="Normal is computed as a 30 years average "
    "starting from the year set via normal_year. <br>"
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Year"],
    operation_id="getYearsAboveNormal",
)
async def get_years_above_normal(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    normal_year: Annotated[
        int, Query(ge=min_year_available, le=max_normal_year_available)
    ],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
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
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["CSV"],
    operation_id="getMinimalCsv",
)
def get_minimal_csv(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    month_value = month.value if time_mode == TimeMode.MONTHLY else None  # type: ignore
    season_value = season.value if time_mode == TimeMode.SEASONAL else None  # type: ignore

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

    filename = f"rainfall_{min_year_available}_{max_year_available}"
    if month_value:
        filename = f"{filename}_{month_value.lower()}"
    elif season_value:
        filename = f"{filename}_{season_value}"

    return StreamingResponse(
        iter(csv_str),
        headers={"Content-Disposition": f'inline; filename="{filename}.csv"'},
        media_type=MediaType.TXT_CSV.value,
    )


@app.get(
    "/graph/rainfall_by_year",
    summary="Retrieve rainfall by year as a PNG or as a JSON.",
    description="Could either be for rainfall upon a whole year, a specific month or a given season.<br>"
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Graph"],
    operation_id="getRainfallByYear",
)
def get_rainfall_by_year(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
    plot_average: bool = False,
    as_json: bool = False,
):
    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    figure = all_rainfall.get_bar_figure_of_rainfall_according_to_year(
        time_mode,
        begin_year=begin_year,
        end_year=end_year,
        month=month.value if month else None,
        season=season.value if season else None,
        plot_average=plot_average,
    )
    if figure is None:
        raise HTTPException(
            status_code=400,
            detail=f"Data has not been successfully plotted, "
            f"check if your data has both '{Label.RAINFALL.value}' and '{Label.YEAR.value}' columns",
        )

    if as_json:
        return figure.to_json()

    img_buffer = io.BytesIO()
    figure.write_image(img_buffer, format="png")
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
    summary="Retrieve rainfall monthly or seasonal averages of data as a PNG or as a JSON.",
    description=f"Time mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.<br>"
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Graph"],
    operation_id="getRainfallAverages",
)
def get_rainfall_averages(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
    as_json: bool = False,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = max_year_available

    raise_year_related_error_or_do_nothing(begin_year, end_year)

    figure = all_rainfall.get_bar_figure_of_rainfall_averages(
        time_mode=time_mode, begin_year=begin_year, end_year=end_year
    )

    if as_json:
        return figure.to_json()

    img_buffer = io.BytesIO()
    figure.write_image(img_buffer, format="png")
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
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Graph"],
    operation_id="getRainfallLinregSlopes",
)
def get_rainfall_linreg_slopes(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
):
    end_year = end_year or max_year_available

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
    f"If no ending year is precised, most recent year available is taken: {max_year_available}.",
    tags=["Graph"],
    operation_id="geRelativeDistancesToNormal",
)
def get_relative_distances_to_normal(
    time_mode: TimeMode,
    normal_year: Annotated[
        int, Query(ge=min_year_available, le=max_normal_year_available)
    ],
    begin_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)],
    end_year: Annotated[int, Query(ge=min_year_available, le=max_year_available)]
    | None = None,
):
    end_year = end_year or max_year_available

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
