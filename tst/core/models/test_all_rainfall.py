from __future__ import annotations

from pathlib import Path
from shutil import rmtree

from src.core.models.all_rainfall import AllRainfall
from src.core.models.monthly_rainfall import MonthlyRainfall
from src.core.models.seasonal_rainfall import SeasonalRainfall
from src.core.models.yearly_rainfall import YearlyRainfall
from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode
from tst.test_config import config

all_rainfall = AllRainfall(config.get_dataset_url())

normal_year: int = 1971
begin_year: int = 1991
end_year: int = 2020

time_mode: str = TimeMode.YEARLY.value
month: str = Month.MAY.name
season: str = Season.SPRING.name


class TestAllRainfall:
    @staticmethod
    def test_export_all_data_to_csv() -> None:
        folder_path: str | None = None
        try:
            folder_path = all_rainfall.export_all_data_to_csv()

            assert isinstance(folder_path, str)
            assert Path(folder_path).exists()
        finally:
            if folder_path:
                rmtree(folder_path, ignore_errors=True)

    @staticmethod
    def test_get_average_rainfall() -> None:
        for t_mode in TimeMode.values():
            avg_rainfall = all_rainfall.get_average_rainfall(
                t_mode, begin_year, end_year, month, season
            )

            assert isinstance(avg_rainfall, float)

    @staticmethod
    def test_get_normal() -> None:
        for t_mode in TimeMode.values():
            normal = all_rainfall.get_normal(t_mode, begin_year, month, season)

            assert isinstance(normal, float)

    @staticmethod
    def test_get_years_below_normal() -> None:
        for t_mode in TimeMode.values():
            n_years_below_avg = all_rainfall.get_years_below_normal(
                t_mode, normal_year, begin_year, end_year, month, season
            )

            assert isinstance(n_years_below_avg, int)
            assert n_years_below_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_above_normal() -> None:
        for t_mode in TimeMode.values():
            n_years_above_avg = all_rainfall.get_years_above_normal(
                t_mode, normal_year, begin_year, end_year, month, season
            )

            assert isinstance(n_years_above_avg, int)
            assert n_years_above_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_last_year() -> None:
        assert isinstance(all_rainfall.get_last_year(), int)

    @staticmethod
    def test_get_relative_distance_from_normal() -> None:
        for t_mode in TimeMode.values():
            relative_distance = all_rainfall.get_relative_distance_from_normal(
                t_mode, normal_year, begin_year, end_year, month, season
            )

            assert isinstance(relative_distance, float)
            assert -100.0 <= relative_distance <= 100.0

    @staticmethod
    def test_get_standard_deviation() -> None:
        for t_mode in TimeMode.values():
            std = all_rainfall.get_rainfall_standard_deviation(
                t_mode, begin_year, end_year, month, season
            )

            assert isinstance(std, float)

    @staticmethod
    def test_get_entity_for_time_mode() -> None:
        assert isinstance(
            all_rainfall.get_entity_for_time_mode(TimeMode.YEARLY), YearlyRainfall
        )
        assert isinstance(
            all_rainfall.get_entity_for_time_mode(
                TimeMode.SEASONAL, season=Season.SPRING.name
            ),
            SeasonalRainfall,
        )
        assert isinstance(
            all_rainfall.get_entity_for_time_mode(
                TimeMode.MONTHLY, month=Month.OCTOBER.name
            ),
            MonthlyRainfall,
        )
        assert all_rainfall.get_entity_for_time_mode("unknown_time_mode") is None
