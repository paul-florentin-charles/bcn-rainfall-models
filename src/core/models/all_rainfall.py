"""
Provides an all-in-one class to manipulate rainfall data for every timeframe.
At a yearly, monthly and seasonal level.
"""

from pathlib import Path

import pandas as pd

from src.config import Config
from src.core.models.monthly_rainfall import MonthlyRainfall
from src.core.models.seasonal_rainfall import SeasonalRainfall
from src.core.models.yearly_rainfall import YearlyRainfall
from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.enums.time_modes import TimeMode
from src.core.utils.functions import plotting


class AllRainfall:
    """
    Provides:
    - YearlyRainfall data
    - MonthlyRainfall data for all months within a dictionary
    - SeasonalRainfall data for all seasons within a dictionary

    A bit costly to instantiate but contains all necessary data.
    """

    def __init__(
        self,
        dataset_url_or_path: str,
        *,
        start_year=1971,
        round_precision=2,
    ):
        self.dataset_url = dataset_url_or_path
        self.starting_year = start_year
        self.round_precision = round_precision
        self.raw_data: pd.DataFrame = pd.read_csv(dataset_url_or_path)
        self.yearly_rainfall = YearlyRainfall(
            self.raw_data, start_year, round_precision
        )
        self.monthly_rainfalls = {
            month.value: MonthlyRainfall(
                self.raw_data, month, start_year, round_precision
            )
            for month in Month
        }
        self.seasonal_rainfalls = {
            season.value: SeasonalRainfall(
                self.raw_data, season, start_year, round_precision
            )
            for season in Season
        }

    @classmethod
    def from_config(cls, from_file=False):
        cfg = Config()

        return cls(
            cfg.get_dataset_path() if from_file else cfg.get_dataset_url(),
            start_year=cfg.get_start_year(),
            round_precision=cfg.get_rainfall_precision(),
        )

    def export_all_data_to_csv(
        self, begin_year: int, end_year: int | None = None, folder_path="csv_data"
    ) -> str:
        """
        Export all the different data as CSVs into specified folder path.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param folder_path: path to folder where to save our CSV files.
        If not set, defaults to 'csv_data'. Should not end with '/'.
        :return: Path to folder that contains CSV files.
        """
        Path(f"{folder_path}/months").mkdir(parents=True, exist_ok=True)
        Path(f"{folder_path}/seasons").mkdir(parents=True, exist_ok=True)

        end_year = end_year or self.yearly_rainfall.get_last_year()

        self.yearly_rainfall.export_as_csv(
            begin_year=begin_year,
            end_year=end_year,
            path=Path(folder_path, f"{begin_year}_{end_year}_rainfall.csv"),
        )

        for monthly_rainfall in self.monthly_rainfalls.values():
            monthly_rainfall.export_as_csv(
                begin_year=begin_year,
                end_year=end_year,
                path=Path(
                    folder_path,
                    "months",
                    f"{begin_year}_{end_year}_{monthly_rainfall.month.value.lower()}_rainfall.csv",
                ),
            )

        for season_rainfall in self.seasonal_rainfalls.values():
            season_rainfall.export_as_csv(
                begin_year=begin_year,
                end_year=end_year,
                path=Path(
                    folder_path,
                    "seasons",
                    f"{begin_year}_{end_year}_{season_rainfall.season.value}_rainfall.csv",
                ),
            )

        return folder_path

    def export_as_csv(
        self,
        time_mode: TimeMode,
        *,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
        path: str | Path | None = None,
    ) -> str | None:
        """
        Export the data state of a specific time mode as a CSV.
        Could be for a yearly time frame, a specific month or a given season.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :param path: path to csv file to save our data (optional).
        :return: CSV data as a string if no path is set.
        None otherwise.
        """
        if entity := self.get_entity_for_time_mode(time_mode, month, season):
            return entity.export_as_csv(
                begin_year=begin_year, end_year=end_year, path=path
            )

        return None

    def get_average_rainfall(
        self,
        time_mode: TimeMode,
        *,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> float | None:
        """
        Computes Rainfall average for a specific year range and time mode.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :return: A float representing the average Rainfall.
        """
        if entity := self.get_entity_for_time_mode(time_mode, month, season):
            return entity.get_average_yearly_rainfall(begin_year, end_year)

        return None

    def get_normal(
        self,
        time_mode: TimeMode,
        begin_year: int,
        month: str | None = None,
        season: str | None = None,
    ) -> float | None:
        """
        Computes Rainfall normal from a specific year and time mode.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param begin_year: An integer representing the year
        to start computing rainfall normal.
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :return: A float representing the Rainfall normal.
        """

        if entity := self.get_entity_for_time_mode(time_mode, month, season):
            return entity.get_normal(begin_year, self.round_precision)

        return None

    def get_relative_distance_from_normal(
        self,
        time_mode: TimeMode,
        normal_year: int,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> float | None:
        """
        Computes relative distance to Rainfall normal for a specific year range and time mode.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :return: A float representing the relative distance to rainfall normal.
        """
        if entity := self.get_entity_for_time_mode(time_mode, month, season):
            return entity.get_relative_distance_from_normal(
                normal_year, begin_year, end_year
            )

        return None

    def get_rainfall_standard_deviation(
        self,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
        weigh_by_average=False,
    ) -> float | None:
        """
        Compute the standard deviation of a column specified by its label within DataFrame
        for a specific year range and time mode.
        By default, it uses the 'Rainfall' column.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :param bool weigh_by_average: whether to divide standard deviation by average or not (optional).
        Default to False.
        :return: The standard deviation as a float.
        Nothing if the specified column does not exist.
        """
        if entity := self.get_entity_for_time_mode(time_mode, month, season):
            return entity.get_standard_deviation(
                begin_year, end_year, weigh_by_average=weigh_by_average
            )

        return None

    def get_years_below_normal(
        self,
        time_mode: TimeMode,
        normal_year: int,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> int | None:
        """
        Computes the number of years below rainfall normal for a specific year range and time mode.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :return: A float representing the relative distance to rainfall normal.
        """
        if entity := self.get_entity_for_time_mode(time_mode, month, season):
            return entity.get_years_below_normal(normal_year, begin_year, end_year)

        return None

    def get_years_above_normal(
        self,
        time_mode: TimeMode,
        normal_year: int,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> int | None:
        """
        Computes the number of years above rainfall normal for a specific year range and time mode.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :return: A float representing the relative distance to rainfall normal.
        """
        if entity := self.get_entity_for_time_mode(time_mode, month, season):
            return entity.get_years_above_normal(normal_year, begin_year, end_year)

        return None

    def get_last_year(self) -> int:
        """
        Retrieves the last element of the 'Year' column from the pandas DataFrames.
        It is a common value for all DataFrames managed by the present class.

        :return: The ultimate year of every DataFrame.
        """

        return self.yearly_rainfall.get_last_year()

    def bar_rainfall_averages(
        self,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int | None = None,
    ) -> list | None:
        """
        Plots a bar graphic displaying average rainfall for each month or each season.

        :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: A list of the Rainfall averages for each month or season.
        None if time_mode is not within {'monthly', 'seasonal'}.
        """
        end_year = end_year or self.get_last_year()
        label = f"Average rainfall (mm) between {begin_year} and {end_year}"

        if time_mode == TimeMode.MONTHLY:
            return plotting.bar_monthly_rainfall_averages(
                list(self.monthly_rainfalls.values()),
                begin_year=begin_year,
                end_year=end_year,
                label=label,
            )
        elif time_mode == TimeMode.SEASONAL:
            return plotting.bar_seasonal_rainfall_averages(
                list(self.seasonal_rainfalls.values()),
                begin_year=begin_year,
                end_year=end_year,
                label=label,
            )

        return None

    def bar_rainfall_linreg_slopes(
        self,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int | None = None,
    ) -> list | None:
        """
        Plots a bar graphic displaying linear regression slope for each month or each season.

        :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        Is set to last year available is None.
        :return: A list of the Rainfall LinReg slopes for each month or season.
        None if time_mode is not within {'monthly', 'seasonal'}.
        """
        end_year = end_year or self.get_last_year()

        if time_mode == TimeMode.MONTHLY:
            return plotting.bar_monthly_rainfall_linreg_slopes(
                list(self.monthly_rainfalls.values()),
                begin_year=begin_year,
                end_year=end_year,
            )
        elif time_mode == TimeMode.SEASONAL:
            return plotting.bar_seasonal_rainfall_linreg_slopes(
                list(self.seasonal_rainfalls.values()),
                begin_year=begin_year,
                end_year=end_year,
            )

        return None

    def get_entity_for_time_mode(
        self, time_mode: TimeMode, month: str | None = None, season: str | None = None
    ) -> YearlyRainfall | MonthlyRainfall | SeasonalRainfall | None:
        """
        Retrieve current entity for specified time mode,
        amongst instances of YearlyRainfall, MonthlyRainfall or SeasonsalRainfall.
        Month or Season should be specified according to time mode.

        :param time_mode: A TimeMode Enum: ['yearly', 'monthly', 'seasonal'].
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional).
        :param season: A string corresponding to the season name.
        Possible values are within ['winter', 'spring', 'summer', 'fall'].
        Set if time_mode is 'seasonal' (optional).
        :return: Corresponding entity as a class instance.
        None if time mode is unknown, time mode is 'monthly' and month is None
        or time mode is 'seasonal' and season is None.
        """
        entity: YearlyRainfall | MonthlyRainfall | SeasonalRainfall | None = None

        if time_mode == TimeMode.YEARLY:
            entity = self.yearly_rainfall
        elif time_mode == TimeMode.MONTHLY and month:
            entity = self.monthly_rainfalls[month]
        elif time_mode == TimeMode.SEASONAL and season:
            entity = self.seasonal_rainfalls[season]

        return entity
