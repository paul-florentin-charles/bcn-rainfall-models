"""
Provides an all-in-one class to manipulate rainfall data for every timeframe.
At a yearly, monthly and seasonal level.
"""

from typing import Optional
from pathlib import Path

import pandas as pd

from src.core.models.monthly_rainfall import MonthlyRainfall
from src.core.models.seasonal_rainfall import SeasonalRainfall
from src.core.models.yearly_rainfall import YearlyRainfall
from src.core.utils.enums.months import Month
from src.core.utils.enums.seasons import Season
from src.core.utils.functions import plotting


class AllRainfall:
    """
    Provides:
    - YearlyRainfall data
    - MonthlyRainfall data for all months
    - SeasonalRainfall data for all seasons

    A bit costly to instantiate but contains all necessary data.
    """

    def __init__(self,
                 dataset_url: str,
                 start_year: Optional[int] = 1971,
                 round_precision: Optional[int] = 2):
        self.dataset_url: str = dataset_url
        self.starting_year: int = start_year
        self.round_precision: int = round_precision
        self.raw_data: pd.DataFrame = pd.read_csv(dataset_url)
        self.yearly_rainfall: YearlyRainfall = YearlyRainfall(self.raw_data,
                                                              start_year,
                                                              round_precision)
        self.monthly_rainfalls: list = []
        for month in Month:
            self.monthly_rainfalls.append(MonthlyRainfall(self.raw_data,
                                                          month,
                                                          start_year,
                                                          round_precision))
        self.seasonal_rainfalls: list = []
        for season in Season:
            self.seasonal_rainfalls.append(SeasonalRainfall(self.raw_data,
                                                            season,
                                                            start_year,
                                                            round_precision))

    def export_all_data_to_csv(self, folder_path: Optional[str] = 'csv_data') -> str:
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
            path=f"{folder_path}/"
                 f"{self.starting_year}_{last_year}_rainfall.csv"
        )

        for monthly_rainfall in self.monthly_rainfalls:
            monthly_rainfall.export_as_csv(
                path=f"{folder_path}/months/"
                     f"{self.starting_year}_{last_year}_"
                     f"{monthly_rainfall.month.name.lower()}_rainfall.csv"
            )

        for season_rainfall in self.seasonal_rainfalls:
            season_rainfall.export_as_csv(
                path=f"{folder_path}/seasons/"
                     f"{self.starting_year}_{last_year}_"
                     f"{season_rainfall.season.name.lower()}_rainfall.csv"
            )

        return folder_path

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
