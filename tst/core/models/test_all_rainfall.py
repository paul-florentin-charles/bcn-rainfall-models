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

ALL_RAINFALL = AllRainfall(config.get_dataset_url())

normal_year = 1971
begin_year = 1991
end_year = 2020

month = Month.MAY.value
season = Season.SPRING.value


class TestAllRainfall:
    @staticmethod
    def test_export_all_data_to_csv():
        folder_path = ""
        try:
            folder_path = ALL_RAINFALL.export_all_data_to_csv()

            assert isinstance(folder_path, str)
            assert Path(folder_path).exists()
        finally:
            if folder_path:
                rmtree(folder_path, ignore_errors=True)

    @staticmethod
    def test_get_average_rainfall():
        for t_mode in TimeMode.values():
            avg_rainfall = ALL_RAINFALL.get_average_rainfall(
                t_mode,
                begin_year=begin_year,
                end_year=end_year,
                month=month,
                season=season,
            )

            assert isinstance(avg_rainfall, float)

    @staticmethod
    def test_get_normal():
        for t_mode in TimeMode.values():
            normal = ALL_RAINFALL.get_normal(t_mode, begin_year, month, season)

            assert isinstance(normal, float)

    @staticmethod
    def test_get_years_below_normal():
        for t_mode in TimeMode.values():
            n_years_below_avg = ALL_RAINFALL.get_years_below_normal(
                t_mode, normal_year, begin_year, end_year, month, season
            )

            assert isinstance(n_years_below_avg, int)
            assert n_years_below_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_above_normal():
        for t_mode in TimeMode.values():
            n_years_above_avg = ALL_RAINFALL.get_years_above_normal(
                t_mode, normal_year, begin_year, end_year, month, season
            )

            assert isinstance(n_years_above_avg, int)
            assert n_years_above_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_last_year():
        assert isinstance(ALL_RAINFALL.get_last_year(), int)

    @staticmethod
    def test_get_relative_distance_from_normal():
        for t_mode in TimeMode.values():
            relative_distance = ALL_RAINFALL.get_relative_distance_from_normal(
                t_mode, normal_year, begin_year, end_year, month, season
            )

            assert isinstance(relative_distance, float)
            assert -100.0 <= relative_distance <= 100.0

    @staticmethod
    def test_get_standard_deviation():
        for t_mode in TimeMode.values():
            std = ALL_RAINFALL.get_rainfall_standard_deviation(
                t_mode, begin_year, end_year, month, season
            )

            assert isinstance(std, float)

    @staticmethod
    def test_get_entity_for_time_mode():
        assert isinstance(
            ALL_RAINFALL.get_entity_for_time_mode(TimeMode.YEARLY.value), YearlyRainfall
        )
        assert isinstance(
            ALL_RAINFALL.get_entity_for_time_mode(
                TimeMode.SEASONAL.value, season=Season.SPRING.value
            ),
            SeasonalRainfall,
        )
        assert isinstance(
            ALL_RAINFALL.get_entity_for_time_mode(
                TimeMode.MONTHLY.value, month=Month.OCTOBER.value
            ),
            MonthlyRainfall,
        )
        assert ALL_RAINFALL.get_entity_for_time_mode("unknown_time_mode") is None
