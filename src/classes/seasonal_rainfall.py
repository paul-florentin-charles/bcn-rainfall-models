"""
Provides a rich class to manipulate Seasonal Rainfall data.
"""

from typing import Optional

import pandas as pd

from src.classes.yearly_rainfall import YearlyRainfall
from src.enums.seasons import Season


class SeasonalRainfall(YearlyRainfall):
    """
    Provides numerous functions to load, manipulate and export Seasonal Rainfall data.
    """

    def __init__(self,
                 season: Season,
                 start_year: Optional[int] = None,
                 round_precision: Optional[int] = None,
                 yearly_rainfall: Optional[pd.DataFrame] = None):
        self.season: Season = season
        super().__init__(start_year, yearly_rainfall, round_precision)

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall for instance season variable into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance season according to year.
        """
        return self.load_rainfall(self.season.value[0].value, self.season.value[2].value + 1)

    def plot_rainfall(self, title: Optional[str] = None) -> None:
        """
        Plot Yearly Rainfall data for the instance season.

        :param title: A string for the plot title (optional)
        :return: None
        """
        if title is None:
            title = f"Barcelona rainfall evolution and various models for " \
                    f"{self.season.name.lower()}"

        super().plot_rainfall(title)

    def plot_normal(self, title: Optional[str] = None) -> None:
        """
        Plot Rainfall normals data for the instance season.

        :param title: A string for the plot title (optional)
        :return: None
        """
        if title is None:
            title = f"Barcelona rainfall evolution compared to normal for " \
                    f"{self.season.name.lower()}"

        super().plot_normal(title)
