"""
Provides a rich class to manipulate Seasonal Rainfall data.
"""

import pandas as pd

from back.core.models.yearly_rainfall import YearlyRainfall
from back.core.utils.enums.seasons import Season


class SeasonalRainfall(YearlyRainfall):
    """
    Provides numerous functions to load, manipulate and export Seasonal Rainfall data.
    """

    def __init__(
        self,
        raw_data: pd.DataFrame,
        season: Season,
        *,
        start_year: int,
        round_precision: int,
    ):
        self.season: Season = season
        super().__init__(
            raw_data, start_year=start_year, round_precision=round_precision
        )

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall for instance season variable into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance season according to year.
        """

        return self.load_rainfall(
            self.season.get_months()[0],
            self.season.get_months()[-1],
        )