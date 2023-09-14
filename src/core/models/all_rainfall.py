"""
Provides a costly to instantiate all-in-one class
to manipulate rainfall data for every timeframes.
"""

from typing import Optional

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

    Costly to instantiate but contains all necessary data.
    """

    def __init__(self,
                 dataset_url: str,
                 start_year: Optional[int] = 1970,
                 round_precision: Optional[int] = 2):
        self.dataset_url: str = dataset_url
        self.starting_year: int = start_year
        self.round_precision: int = round_precision
        self.yearly_rainfall: YearlyRainfall = YearlyRainfall(dataset_url,
                                                              start_year,
                                                              round_precision)
        self.monthly_rainfalls: list = []
        for month in Month:
            self.monthly_rainfalls.append(MonthlyRainfall(dataset_url,
                                                          month,
                                                          start_year,
                                                          round_precision))
        self.seasonal_rainfalls: list = []
        for season in Season:
            self.seasonal_rainfalls.append(SeasonalRainfall(dataset_url,
                                                            season,
                                                            start_year,
                                                            round_precision))

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
