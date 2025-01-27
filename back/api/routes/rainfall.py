from typing import Annotated

from fastapi import Query

from back.api.routes import (
    MAX_NORMAL_YEAR_AVAILABLE,
    MAX_YEAR_AVAILABLE,
    MIN_YEAR_AVAILABLE,
    all_rainfall,
)
from back.api.utils import (
    RainfallModel,
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)
from back.rainfall.utils import Month, Season, TimeMode


async def get_rainfall_average(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
        name="rainfall average (mm)",
        value=all_rainfall.get_rainfall_average(
            time_mode,
            begin_year=begin_year,
            end_year=end_year,
            month=month,
            season=season,
        ),  # type: ignore
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


async def get_rainfall_normal(
    time_mode: TimeMode,
    begin_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
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
            month=month,
            season=season,
        ),  # type: ignore
        begin_year=begin_year,
        end_year=begin_year + 29,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


async def get_rainfall_relative_distance_to_normal(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    normal_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
    ],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
        name="relative distance to rainfall normal (%)",
        value=all_rainfall.get_relative_distance_to_normal(
            time_mode,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
            month=month,
            season=season,
        ),  # type: ignore
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )


async def get_rainfall_standard_deviation(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
    weigh_by_average: bool = False,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    return RainfallModel(
        name=f"rainfall standard deviation {"weighted by average" if weigh_by_average else "(mm)"}",
        value=all_rainfall.get_rainfall_standard_deviation(
            time_mode,
            begin_year=begin_year,
            end_year=end_year,
            month=month,
            season=season,
            weigh_by_average=weigh_by_average,
        ),  # type: ignore
        begin_year=begin_year,
        end_year=end_year,
        time_mode=time_mode,
        month=month if time_mode == TimeMode.MONTHLY else None,
        season=season if time_mode == TimeMode.SEASONAL else None,
    )
