"""
Provides an all-in-one class to manipulate rainfall data for every timeframe.
At a yearly, monthly and seasonal level.
"""

from pathlib import Path
from typing import Optional, Union

import pandas as pd

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
        dataset_url: str,
        start_year: Optional[int] = 1971,
        round_precision: Optional[int] = 2,
    ):
        self.dataset_url: str = dataset_url
        self.starting_year: int = start_year
        self.round_precision: int = round_precision
        self.raw_data: pd.DataFrame = pd.read_csv(dataset_url)
        self.yearly_rainfall: YearlyRainfall = YearlyRainfall(
            self.raw_data, start_year, round_precision
        )
        self.monthly_rainfalls: dict = {}
        for month in Month:
            self.monthly_rainfalls[month.name] = MonthlyRainfall(
                self.raw_data, month, start_year, round_precision
            )
        self.seasonal_rainfalls: dict = {}
        for season in Season:
            self.seasonal_rainfalls[season.name] = SeasonalRainfall(
                self.raw_data, season, start_year, round_precision
            )

    def export_all_data_to_csv(self, folder_path: Optional[str] = "csv_data") -> str:
        """
        Export all the different data as CSVs into specified folder path.

        :param folder_path: path to folder where to save our CSV files (optional).
        If not set, defaults to 'csv_data'. Should not end with '/'.
        :return: Path to folder that contains CSV files.
        """
        Path(f"{folder_path}/months").mkdir(parents=True, exist_ok=True)
        Path(f"{folder_path}/seasons").mkdir(parents=True, exist_ok=True)

        last_year: int = self.yearly_rainfall.get_last_year()

        self.yearly_rainfall.export_as_csv(
            path=f"{folder_path}/" f"{self.starting_year}_{last_year}_rainfall.csv"
        )

        for monthly_rainfall in self.monthly_rainfalls.values():
            monthly_rainfall.export_as_csv(
                path=f"{folder_path}/months/"
                f"{self.starting_year}_{last_year}_"
                f"{monthly_rainfall.month.name.lower()}_rainfall.csv"
            )

        for season_rainfall in self.seasonal_rainfalls.values():
            season_rainfall.export_as_csv(
                path=f"{folder_path}/seasons/"
                f"{self.starting_year}_{last_year}_"
                f"{season_rainfall.season.name.lower()}_rainfall.csv"
            )

        return folder_path

    def export_as_csv(
        self,
        time_mode: str,
        month: Optional[str] = None,
        season: Optional[str] = None,
        path: Optional[str] = None,
    ) -> Union[str, None]:
        """
        Export the data state of a specific time mode as a CSV.
        Could be for a yearly time frame, a specific month or a given season.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        Set if time_mode is 'seasonal' (optional)
        :param path: path to csv file to save our data (optional).
        :return: CSV data as a string if no path is set.
        None otherwise.
        """
        entity = self.get_entity_for_time_mode(time_mode, month, season)

        if entity is None:
            return entity

        return entity.export_as_csv(path)

    def get_average_rainfall(
        self,
        time_mode: str,
        begin_year: Optional[int] = None,
        end_year: Optional[int] = None,
        month: Optional[str] = None,
        season: Optional[str] = None,
    ) -> Union[float, None]:
        """
        Computes Rainfall average for a specific year range and time mode.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        Set if time_mode is 'seasonal' (optional)
        :return: A float representing the average Rainfall.
        """
        entity = self.get_entity_for_time_mode(time_mode, month, season)

        if entity is None:
            return entity

        return entity.get_average_yearly_rainfall(begin_year, end_year)

    def get_normal(
        self,
        time_mode: str,
        begin_year: int,
        month: Optional[str] = None,
        season: Optional[str] = None,
    ) -> Union[float, None]:
        """
        Computes Rainfall normal from a specific year and time mode.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param begin_year: An integer representing the year
        to start computing rainfall normal.
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        Set if time_mode is 'seasonal' (optional)
        :return: A float representing the Rainfall normal.
        """

        entity = self.get_entity_for_time_mode(time_mode, month, season)

        if entity is None:
            return entity

        return entity.get_normal(begin_year)

    def get_relative_distance_from_normal(
        self,
        time_mode: str,
        normal_year: int,
        begin_year: int,
        end_year: Optional[int] = None,
        month: Optional[str] = None,
        season: Optional[str] = None,
    ) -> Union[float, None]:
        """
        Computes relative distance to Rainfall normal for a specific year range and time mode.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        Set if time_mode is 'seasonal' (optional)
        :return: A float representing the relative distance to rainfall normal.
        """
        entity = self.get_entity_for_time_mode(time_mode, month, season)

        if entity is None:
            return entity

        return entity.get_relative_distance_from_normal(
            normal_year, begin_year, end_year
        )

    def get_rainfall_standard_deviation(
        self,
        time_mode: str,
        begin_year: int,
        end_year: Optional[int] = None,
        month: Optional[str] = None,
        season: Optional[str] = None,
    ) -> Union[float, None]:
        """
        Compute the standard deviation of a column specified by its label within DataFrame
        for a specific year range and time mode.
        By default, it uses the 'Rainfall' column.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        Set if time_mode is 'seasonal' (optional)
        :return: The standard deviation as a float.
        Nothing if the specified column does not exist.
        """
        entity = self.get_entity_for_time_mode(time_mode, month, season)

        if entity is None:
            return entity

        return entity.get_standard_deviation(begin_year, end_year)

    def get_years_below_normal(
        self,
        time_mode: str,
        normal_year: int,
        begin_year: int,
        end_year: Optional[int] = None,
        month: Optional[str] = None,
        season: Optional[str] = None,
    ) -> Union[int, None]:
        """
        Computes the number of years below rainfall normal for a specific year range and time mode.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        Set if time_mode is 'seasonal' (optional)
        :return: A float representing the relative distance to rainfall normal.
        """
        entity = self.get_entity_for_time_mode(time_mode, month, season)

        if entity is None:
            return entity

        return entity.get_years_below_normal(normal_year, begin_year, end_year)

    def get_years_above_normal(
        self,
        time_mode: str,
        normal_year: int,
        begin_year: int,
        end_year: Optional[int] = None,
        month: Optional[str] = None,
        season: Optional[str] = None,
    ) -> Union[int, None]:
        """
        Computes the number of years above rainfall normal for a specific year range and time mode.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        Set if time_mode is 'seasonal' (optional)
        :return: A float representing the relative distance to rainfall normal.
        """
        entity = self.get_entity_for_time_mode(time_mode, month, season)

        if entity is None:
            return entity

        return entity.get_years_above_normal(normal_year, begin_year, end_year)

    def get_last_year(self) -> int:
        """
        Retrieves the last element of the 'Year' column from the pandas DataFrames.
        It is a common value for all DataFrames managed by the present class.

        :return: The ultimate year of every DataFrame.
        """

        return self.yearly_rainfall.get_last_year()

    def bar_rainfall_averages(self, monthly: Optional[bool] = True) -> list:
        """
        Plots a bar graphic displaying average rainfall for each month or each season.

        :param monthly: if True, plots monthly rainfall averages.
        if False, plots seasonal rainfall averages.
        :return: A list of the Rainfall averages for each month or season.
        """
        if monthly:
            return plotting.bar_monthly_rainfall_averages(self.monthly_rainfalls)

        return plotting.bar_seasonal_rainfall_averages(self.seasonal_rainfalls)

    def bar_rainfall_linreg_slopes(self, monthly: Optional[bool] = True) -> list:
        """
        Plots a bar graphic displaying linear regression slope for each month or each season.

        :param monthly: if True, plots monthly rainfall LinReg slopes.
        if False, plots seasonal rainfall LinReg slopes.
        :return: A list of the Rainfall LinReg slopes for each month or season.
        """
        if monthly:
            return plotting.bar_monthly_rainfall_linreg_slopes(self.monthly_rainfalls)

        return plotting.bar_seasonal_rainfall_linreg_slopes(self.seasonal_rainfalls)

    def get_entity_for_time_mode(
        self, time_mode: str, month: Optional[str], season: Optional[str]
    ) -> Union[YearlyRainfall, MonthlyRainfall, SeasonalRainfall, None]:
        """
        Retrieve current entity for specified time mode,
        amongst instances of YearlyRainfall, MonthlyRainfall or SeasonsalRainfall.
        Month or Season should be specified according to time mode.

        :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
        :param month: A string corresponding to the month name.
        Set if time_mode is 'monthly' (optional)
        :param season: A string corresponding to the season name.
        Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
        :return: Corresponding entity as a class instance.
        None if time mode is unknown.
        """
        entity: Union[YearlyRainfall, MonthlyRainfall, SeasonalRainfall, None] = None

        if time_mode.casefold() == TimeMode.YEARLY.value.casefold():
            entity = self.yearly_rainfall
        elif time_mode.casefold() == TimeMode.MONTHLY.value.casefold():
            entity = self.monthly_rainfalls[month.upper()]
        elif time_mode.casefold() == TimeMode.SEASONAL.value.casefold():
            entity = self.seasonal_rainfalls[season.upper()]

        return entity
