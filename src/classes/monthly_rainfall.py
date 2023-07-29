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

    def plot_rainfall(self, title: Optional[str] = None) -> None:
        """
        Plot Yearly Rainfall data for the instance month.

        :param title: A string for the plot title (optional)
        :return: None
        """
        if title is None:
            title = f"Barcelona rainfall evolution and various models for " \
                    f"{self.month.name.capitalize()}"

        super().plot_rainfall(title)

    def plot_normal(self,
                    title: Optional[str] = None,
                    kmeans_clusters: Optional[int] = None) -> None:
        """
        Plot Rainfall normals data for the instance month.

        :param kmeans_clusters: The number of clusters to display
        :param title: A string for the plot title (optional)
        :return: None
        """
        if title is None:
            title = f"Barcelona rainfall evolution compared to normal for " \
                    f"{self.month.name.capitalize()}"

        super().plot_normal(title, kmeans_clusters)
