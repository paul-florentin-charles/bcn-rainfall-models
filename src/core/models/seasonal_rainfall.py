"""
Provides a rich class to manipulate Seasonal Rainfall data.
"""

from typing import Optional

import pandas as pd

from src.core.models.yearly_rainfall import YearlyRainfall
from src.core.utils.enums.seasons import Season


class SeasonalRainfall(YearlyRainfall):
    """
    Provides numerous functions to load, manipulate and export Seasonal Rainfall data.
    """

    def __init__(
        self,
        raw_data: pd.DataFrame,
        season: Season,
        start_year: Optional[int] = 1971,
        round_precision: Optional[int] = 2,
    ):
        self.season: Season = season
        super().__init__(raw_data, start_year, round_precision)

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall for instance season variable into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance season according to year.
        """

        return self.load_rainfall(
            self.season.value[0].value, self.season.value[2].value + 1
        )
