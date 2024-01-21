"""
Provides a rich class to manipulate Monthly Rainfall data.
"""
from __future__ import annotations

import pandas as pd

from src.core.models.yearly_rainfall import YearlyRainfall
from src.core.utils.enums.months import Month


class MonthlyRainfall(YearlyRainfall):
    """
    Provides numerous functions to load, manipulate and export Monthly Rainfall data.
    """

    def __init__(
        self,
        raw_data: pd.DataFrame,
        month: Month,
        start_year: int | None = 1971,
        round_precision: int | None = 2,
    ):
        self.month: Month = month
        super().__init__(raw_data, start_year, round_precision)

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall for instance month variable into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance month according to year.
        """

        return self.load_rainfall(self.month.value, self.month.value + 1)
