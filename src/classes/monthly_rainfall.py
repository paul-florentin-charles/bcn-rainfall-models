"""
Provides a rich class to manipulate Monthly Rainfall data.
"""

from typing import Optional

import pandas as pd

from src.classes.yearly_rainfall import YearlyRainfall
from src.enums.months import Month


class MonthlyRainfall(YearlyRainfall):
    """
    Provides numerous functions to load, manipulate and export Monthly Rainfall data.
    """

    def __init__(self,
                 dataset_url: str,
                 month: Month,
                 start_year: Optional[int] = 1970,
                 round_precision: Optional[int] = 2):
        self.month: Month = month
        super().__init__(dataset_url, start_year, round_precision)

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall for instance month variable into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance month according to year.
        """

        return self.load_rainfall(self.month.value, self.month.value + 1)
