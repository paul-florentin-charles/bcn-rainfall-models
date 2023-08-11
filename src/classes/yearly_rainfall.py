"""
Provides a rich class to manipulate Yearly Rainfall data.
"""

import operator as opr
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from src.decorators import plots
from src.enums.labels import Label
from src.enums.months import Month
from src.utils import metrics, dataframe_operations as df_opr


class YearlyRainfall:
    """
    Provides numerous functions to load, manipulate and export Yearly Rainfall data.
    """

    def __init__(self,
                 dataset_url: str,
                 start_year: Optional[int] = 1970,
                 round_precision: Optional[int] = 2):
        self.dataset_url: str = dataset_url
        self.starting_year: int = start_year
        self.round_precision: int = round_precision
        self.data: pd.DataFrame = self.load_yearly_rainfall()

    def __str__(self):
        return self.data.to_string()

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
        monthly_rainfall: pd.DataFrame = pd.read_csv(self.dataset_url)

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

        yearly_rainfall = df_opr.get_rainfall_within_year_interval(yearly_rainfall,
                                                                   begin_year=self.starting_year) \
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

        return df_opr.get_rainfall_within_year_interval(self.data,
                                                        begin_year,
                                                        end_year)

    def export_as_csv(self, path: Optional[str] = None) -> str:
        """
        Export the actual instance data state as a CSV.

        :param path: path to csv file to save our data (optional).
        :return: CSV data as a string.
        """
        return self.data.to_csv(path_or_buf=path, index=False)

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

        return metrics.get_average_rainfall(self.get_yearly_rainfall(begin_year, end_year),
                                            self.round_precision)

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

        return metrics.get_years_compared_to_given_rainfall_value(
            self.get_yearly_rainfall(begin_year, end_year),
            self.get_average_yearly_rainfall(begin_year, end_year),
            opr.lt
        )

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

        return metrics.get_years_compared_to_given_rainfall_value(
            self.get_yearly_rainfall(begin_year, end_year),
            self.get_average_yearly_rainfall(begin_year, end_year),
            opr.gt
        )

    def get_standard_deviation(self,
                               label: Optional[Label] = Label.RAINFALL,
                               begin_year: Optional[int] = None,
                               end_year: Optional[int] = None) -> Union[float, None]:
        """
        Compute the standard deviation of a column specified by its label within DataFrame
        and for an optional time range.
        By default, it uses the 'Rainfall' column.

        :param label: A string corresponding to an existing column label (optional).
        :param begin_year: An integer representing the year
        to start getting our rainfall values (optional).
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: The standard deviation as a float.
        Nothing if the specified column does not exist.
        """
        if label not in self.data.columns:
            return None

        return round(self.get_yearly_rainfall(begin_year, end_year)[label].std(),
                     self.round_precision)

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

        self.data[Label.PERCENTAGE_OF_NORMAL.value] = round(
            self.data[Label.RAINFALL.value] / normal * 100.0, self.round_precision)

    def add_linear_regression(self) -> (float, float):
        """
        Compute and add Linear Regression of Rainfall according to Year
        to our pandas DataFrame.

        :return: a tuple containing two floats (r2 score, slope).
        """
        years: np.ndarray = self.data[Label.YEAR.value].values.reshape(-1, 1)
        rainfalls: np.ndarray = self.data[Label.RAINFALL.value].values

        reg: LinearRegression = LinearRegression()
        reg.fit(years, rainfalls)
        self.data[Label.LINEAR_REGRESSION.value] = reg.predict(years)
        self.data[Label.LINEAR_REGRESSION.value] = round(
            self.data[Label.LINEAR_REGRESSION.value], self.round_precision)

        return r2_score(rainfalls,
                        self.data[Label.LINEAR_REGRESSION.value].values), \
            reg.coef_[0]

    def add_savgol_filter(self) -> None:
        """
        Compute and add Savitzky–Golay filter to Rainfall according to Year
        to our pandas DataFrame.

        :return: None
        """
        self.data[Label.SAVITZKY_GOLAY_FILTER.value] = signal.savgol_filter(
            self.data[Label.RAINFALL.value],
            window_length=len(self.data),
            polyorder=len(
                self.data) // 10)

        self.data[Label.SAVITZKY_GOLAY_FILTER.value] = round(
            self.data[Label.SAVITZKY_GOLAY_FILTER.value], self.round_precision)

    def add_kmeans(self, kmeans_clusters: Optional[int] = 4) -> int:
        """
        Compute and add K-Mean clustering of Rainfall according to Year
        to our pandas DataFrame.

        :param kmeans_clusters: The number of clusters to compute (optional)
        :return: The number of computed clusters as an integer
        """
        fit_data: np.ndarray = self.data[[Label.YEAR.value, Label.RAINFALL.value]].values

        kmeans: KMeans = KMeans(n_init=10, n_clusters=kmeans_clusters)
        kmeans.fit(fit_data)
        self.data[Label.KMEANS.value] = kmeans.predict(fit_data)

        return kmeans.n_clusters

    def remove_column(self, label: Label) -> bool:
        """
        Remove a column for DataFrame using its label.
        Removing 'Year' or 'Rainfall' columns is prevented.

        :param label: A string corresponding to an existing column label.
        :return: A boolean set to whether the operation passed or not.
        """
        if label not in self.data.columns.drop([Label.YEAR, Label.RAINFALL]):
            return False

        self.data = self.data.drop(label.value, axis='columns')

        return True

    @plots.legend_and_show()
    def plot_rainfall(self, title: Optional[str] = None) -> None:
        """
        Plot Yearly Rainfall data.

        :param title: A string for the plot title (optional)
        :return: None
        """
        for column_label in self.data.columns[1:]:
            if column_label in [Label.PERCENTAGE_OF_NORMAL, Label.KMEANS]:
                continue

            plt.plot(self.data[Label.YEAR.value],
                     self.data[column_label],
                     label=column_label)

        if title is not None:
            plt.title(title)
        else:
            plt.title("Barcelona rainfall evolution and various models")

    @plots.legend_and_show(ylabel=Label.PERCENTAGE_OF_NORMAL.value)
    def plot_normal(self,
                    title: Optional[str] = None,
                    kmeans_clusters: Optional[int] = None) -> None:
        """
        Plot Rainfall normals data.

        :param kmeans_clusters: The number of clusters to display
        :param title: A string for the plot title (optional)
        :return: None
        """
        if Label.PERCENTAGE_OF_NORMAL not in self.data.columns:
            return

        plt.axhline(y=100.0, color='orange', linestyle='dashed', label='Normal')
        if Label.KMEANS.value not in self.data.columns or kmeans_clusters is None:
            plt.scatter(self.data[Label.YEAR.value],
                        self.data[Label.PERCENTAGE_OF_NORMAL.value],
                        label=Label.PERCENTAGE_OF_NORMAL.value)
        else:
            year_rain: pd.DataFrame = self.data
            for label_value in range(kmeans_clusters):
                year_rain = year_rain[year_rain[Label.KMEANS.value] == label_value]
                plt.scatter(year_rain[Label.YEAR.value],
                            year_rain[Label.PERCENTAGE_OF_NORMAL.value])
                year_rain = self.data

        if title is not None:
            plt.title(title)
        else:
            plt.title("Barcelona rainfall evolution compared to normal")
