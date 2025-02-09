from typing import Annotated

from fastapi import HTTPException, Query

from back.api.routes import (
    MAX_NORMAL_YEAR_AVAILABLE,
    MAX_YEAR_AVAILABLE,
    MIN_YEAR_AVAILABLE,
    all_rainfall,
)
from back.api.utils import (
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)
from back.rainfall.utils import Label, Month, Season, TimeMode


def get_rainfall_by_year_as_plotly_json(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
    plot_average: bool = False,
    plot_linear_regression: bool = False,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(begin_year, end_year)
    raise_time_mode_error_or_do_nothing(time_mode, month, season)

    figure = all_rainfall.get_bar_figure_of_rainfall_according_to_year(
        time_mode,
        begin_year=begin_year,
        end_year=end_year,
        month=month,
        season=season,
        plot_average=plot_average,
        plot_linear_regression=plot_linear_regression,
    )
    if figure is None:
        raise HTTPException(
            status_code=400,
            detail=f"Data has not been successfully plotted, "
            f"check if your data has both '{Label.RAINFALL.value}' and '{Label.YEAR.value}' columns",
        )

    return figure.to_json()


def get_rainfall_averages_as_plotly_json(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(begin_year, end_year)

    figure = all_rainfall.get_bar_figure_of_rainfall_averages(
        time_mode=time_mode, begin_year=begin_year, end_year=end_year
    )

    return figure.to_json()


def get_rainfall_linreg_slopes_as_plotly_json(
    time_mode: TimeMode,
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    raise_year_related_error_or_do_nothing(begin_year, end_year)

    figure = all_rainfall.get_bar_figure_of_rainfall_linreg_slopes(
        time_mode=time_mode, begin_year=begin_year, end_year=end_year
    )

    return figure.to_json()


def get_relative_distances_to_normal_as_plotly_json(
    time_mode: TimeMode,
    normal_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
    ],
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
):
    if time_mode == TimeMode.YEARLY:
        raise HTTPException(
            status_code=400,
            detail=f"time_mode should be either '{TimeMode.MONTHLY.value}' or '{TimeMode.SEASONAL.value}'.",
        )

    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    figure = all_rainfall.get_bar_figure_of_relative_distance_to_normal(
        time_mode=time_mode,
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
    )

    return figure.to_json()


def get_pourcentage_of_years_above_and_below_normal_as_plotly_json(
    time_mode: TimeMode,
    normal_year: Annotated[
        int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_NORMAL_YEAR_AVAILABLE)
    ],
    begin_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)],
    end_year: Annotated[int, Query(ge=MIN_YEAR_AVAILABLE, le=MAX_YEAR_AVAILABLE)]
    | None = None,
    month: Month | None = None,
    season: Season | None = None,
):
    if end_year is None:
        end_year = MAX_YEAR_AVAILABLE

    figure = all_rainfall.get_pie_figure_of_years_above_and_below_normal(
        time_mode=time_mode,
        normal_year=normal_year,
        begin_year=begin_year,
        end_year=end_year,
        month=month,
        season=season,
    )

    return figure.to_json()
