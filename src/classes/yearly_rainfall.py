"""
Provides a rich class to manipulate Yearly Rainfall data.
"""

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.cluster import KMeans

from src.config import Config
from src.decorators import plots
from src.enums.labels import Label
from src.enums.months import Month


class YearlyRainfall:
    """
    Provides numerous functions to load, manipulate and export Yearly Rainfall data.
    """

    def __init__(self,
                 start_year: Optional[int] = None,
                 yearly_rainfall: Optional[pd.DataFrame] = None):
        cfg: Config = Config()
        self.starting_year: int = cfg.get_start_year() \
            if start_year is None \
            else start_year
        self.round_precision: int = cfg.get_rainfall_precision()
        self.yearly_rainfall: pd.DataFrame = self.load_yearly_rainfall() \
            if yearly_rainfall is None \
            else yearly_rainfall

    def __str__(self):
        return self.yearly_rainfall.to_string()

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm) according to year.
        """
        return self.load_rainfall(Month.JANUARY.value)

    def load_rainfall(self,
                      start_month: int,
                      end_month: Optional[int] = None) -> pd.DataFrame:
        """
        Generic function to load Yearly Rainfall data into pandas DataFrame.

        :param start_month: An integer representing the month
        to start getting our rainfall values (compulsory)
        :param end_month: An integer representing the month
        to end getting our rainfall values (optional)
        :return: A pandas DataFrame displaying rainfall data (in mm) according to year.
        """
        monthly_rainfall: pd.DataFrame = pd.read_csv(Config().get_dataset_url())

        years: pd.DataFrame = monthly_rainfall.iloc[:, :1]
        if end_month is not None and end_month < start_month:
            rainfall: pd.Series = pd.concat(
                (monthly_rainfall.iloc[:, start_month:start_month + 1],
                 monthly_rainfall.iloc[:, 1:end_month]), axis='columns') \
                .sum(axis='columns')
        else:
            rainfall: pd.Series = monthly_rainfall.iloc[:, start_month:end_month] \
                .sum(axis='columns')

        yearly_rainfall: pd.DataFrame = pd.concat((years, rainfall), axis='columns') \
            .set_axis([Label.YEAR.value, Label.RAINFALL.value],
                      axis='columns')

        if self.starting_year is not None:
            yearly_rainfall = yearly_rainfall[
                yearly_rainfall[Label.YEAR.value] >= self.starting_year
                ] \
                .reset_index() \
                .drop(columns='index')

        yearly_rainfall[Label.RAINFALL.value] = round(yearly_rainfall[Label.RAINFALL.value],
                                                      self.round_precision)

        return yearly_rainfall

    def get_yearly_rainfall(self,
                            begin_year: Optional[int] = None,
                            end_year: Optional[int] = None) -> pd.DataFrame:
        """
        Retrieves Yearly Rainfall within a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance month according to year.
        """
        year_rain: pd.DataFrame = self.yearly_rainfall

        if begin_year is not None:
            year_rain = year_rain[year_rain[Label.YEAR.value] >= begin_year]

        if end_year is not None:
            year_rain = year_rain[year_rain[Label.YEAR.value] <= end_year]

        return year_rain

    def export_as_csv(self, path: Optional[str] = None) -> str:
        """
        Export the actual instance data state as a CSV.

        :param path: path to csv file to save our data (optional).
        :return: CSV data as a string.
        """
        return self.yearly_rainfall.to_csv(path_or_buf=path, index=False)

    def get_average_yearly_rainfall(self,
                                    begin_year: Optional[int] = None,
                                    end_year: Optional[int] = None) -> float:
        """
        Computes Rainfall average for a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: A float representing the average Rainfall.
        """
        year_rain: pd.DataFrame = self.get_yearly_rainfall(begin_year, end_year)

        nb_years: int = len(year_rain)
        if nb_years == 0:
            return 0.

        year_rain = year_rain.sum(axis='rows')

        return round(year_rain.loc[Label.RAINFALL.value] / nb_years, self.round_precision)

    def get_years_below_average(self,
                                begin_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> int:
        """
        Computes the number of years below average rainfall for a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: The number of years below the computed average as an integer.
        """
        normal: float = self.get_average_yearly_rainfall(begin_year, end_year)

        year_rain: pd.DataFrame = self.get_yearly_rainfall(begin_year, end_year)
        year_rain = year_rain[year_rain[Label.RAINFALL.value] < normal]

        return year_rain.count()[Label.YEAR.value]

    def get_years_above_average(self,
                                begin_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> int:
        """
        Computes the number of years above average rainfall for a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: The number of years above the computed average as an integer.
        """
        normal: float = self.get_average_yearly_rainfall(begin_year, end_year)

        year_rain: pd.DataFrame = self.get_yearly_rainfall(begin_year, end_year)
        year_rain = year_rain[year_rain[Label.RAINFALL.value] > normal]

        return year_rain.count()[Label.YEAR.value]

    def add_percentage_of_normal(self,
                                 begin_year: Optional[int] = None,
                                 end_year: Optional[int] = None) -> None:
        """
        Add the percentage of rainfall compared with normal
        to our pandas DataFrame for a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: None
        """
        normal: float = self.get_average_yearly_rainfall(begin_year, end_year)
        if normal == 0.:
            return

        self.yearly_rainfall[Label.PERCENTAGE_OF_NORMAL.value] = round(
            self.yearly_rainfall[Label.RAINFALL.value] / normal * 100.0, self.round_precision)

    def add_linear_regression(self) -> (float, float):
        """
        Compute and add Linear Regression of Rainfall according to Year
        to our pandas DataFrame.

        :return: a tuple containing two floats (r2 score, slope).
        """
        years: np.ndarray = self.yearly_rainfall[Label.YEAR.value].values.reshape(-1, 1)
        rainfalls: np.ndarray = self.yearly_rainfall[Label.RAINFALL.value].values

        reg: LinearRegression = LinearRegression()
        reg.fit(years, rainfalls)
        self.yearly_rainfall[Label.LINEAR_REGRESSION.value] = reg.predict(years)
        self.yearly_rainfall[Label.LINEAR_REGRESSION.value] = round(
            self.yearly_rainfall[Label.LINEAR_REGRESSION.value], self.round_precision)

        return r2_score(rainfalls,
                        self.yearly_rainfall[Label.LINEAR_REGRESSION.value].values), \
            reg.coef_[0]

    def add_savgol_filter(self) -> None:
        """
        Compute and add Savitzky–Golay filter to Rainfall according to Year
        to our pandas DataFrame.

        :return: None
        """
        self.yearly_rainfall[Label.SAVITZKY_GOLAY_FILTER.value] = signal.savgol_filter(
            self.yearly_rainfall[Label.RAINFALL.value],
            window_length=len(self.yearly_rainfall),
            polyorder=len(
                self.yearly_rainfall) // 10)

        self.yearly_rainfall[Label.SAVITZKY_GOLAY_FILTER.value] = round(
            self.yearly_rainfall[Label.SAVITZKY_GOLAY_FILTER.value], self.round_precision)

    def add_kmeans(self) -> None:
        """
        Compute and add K-Mean clustering of Rainfallc according to Year
        to our pandas DataFrame.

        :return: None
        """
        fit_data: np.ndarray = self.yearly_rainfall[[Label.YEAR.value, Label.RAINFALL.value]].values

        kmeans: KMeans = KMeans(n_init=10, n_clusters=Config().get_kmeans_clusters())
        kmeans.fit(fit_data)
        self.yearly_rainfall[Label.KMEANS.value] = kmeans.predict(fit_data)

    @plots.legend_and_show()
    def plot_rainfall(self, title: Optional[str] = None) -> None:
        """
        Plot Yearly Rainfall data.

        :param title: A string for the plot title (optional)
        :return: None
        """
        for column_label in self.yearly_rainfall.columns[1:]:
            if column_label in [Label.PERCENTAGE_OF_NORMAL.value, Label.KMEANS.value]:
                continue

            plt.plot(self.yearly_rainfall[Label.YEAR.value],
                     self.yearly_rainfall[column_label],
                     label=column_label)

        if title is not None:
            plt.title(title)
        else:
            plt.title("Barcelona rainfall evolution and various models")

    @plots.legend_and_show()
    def plot_normal(self, title: Optional[str] = None) -> None:
        """
        Plot Rainfall normals data.

        :param title: A string for the plot title (optional)
        :return: None
        """
        if Label.PERCENTAGE_OF_NORMAL.value not in self.yearly_rainfall.columns:
            return

        plt.axhline(y=100.0, color='orange', linestyle='dashed', label='Normal')
        if Label.KMEANS.value not in self.yearly_rainfall.columns:
            plt.scatter(self.yearly_rainfall[Label.YEAR.value],
                        self.yearly_rainfall[Label.PERCENTAGE_OF_NORMAL.value],
                        label=Label.PERCENTAGE_OF_NORMAL.value)
        else:
            year_rain: pd.DataFrame = self.yearly_rainfall
            for label_value in range(Config().get_kmeans_clusters()):
                year_rain = year_rain[year_rain[Label.KMEANS.value] == label_value]
                plt.scatter(year_rain[Label.YEAR.value],
                            year_rain[Label.PERCENTAGE_OF_NORMAL.value])
                year_rain = self.yearly_rainfall

        if title is not None:
            plt.title(title)
        else:
            plt.title("Barcelona rainfall evolution compared to normal")
