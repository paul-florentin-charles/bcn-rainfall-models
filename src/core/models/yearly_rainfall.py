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

from src.core.utils.decorators import plots
from src.core.utils.enums.labels import Label
from src.core.utils.enums.months import Month
from src.core.utils.functions import dataframe_operations as df_opr, metrics, plotting


class YearlyRainfall:
    """
    Provides numerous functions to load, manipulate and export Yearly Rainfall data.
    """

    def __init__(self,
                 raw_data: pd.DataFrame,
                 start_year: Optional[int] = 1970,
                 round_precision: Optional[int] = 2):
        self.raw_data: pd.DataFrame = raw_data
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
        Generic function to load Yearly Rainfall data from raw data stored in pandas DataFrame.
        Raw data has to be shaped as rainfall values for each month according to year.

        :param start_month: An integer representing the month
        to start getting our rainfall values (compulsory)
        :param end_month: An integer representing the month
        to end getting our rainfall values (optional)
        :return: A pandas DataFrame displaying rainfall data (in mm) according to year.
        """

        return df_opr.retrieve_rainfall_data_with_constraints(self.raw_data,
                                                              self.starting_year,
                                                              self.round_precision,
                                                              start_month,
                                                              end_month)

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

    def export_as_csv(self, path: Optional[str] = None) -> Union[str, None]:
        """
        Export the actual instance data state as a CSV.

        :param path: path to csv file to save our data (optional).
        :return: CSV data as a string if no path is set.
        None otherwise.
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

    def get_normal(self, begin_year) -> float:
        """
        Computes Rainfall average over 30 years time frame.

        :param begin_year: An integer representing the year
        to start from to compute our normal.
        :return: A float storing the normal.
        """

        return metrics.get_normal(self.data, begin_year)

    def get_years_below_normal(self,
                               normal_year: int,
                               begin_year: int,
                               end_year: Optional[int] = None) -> int:
        """
        Computes the number of years below normal for a specific year range.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: The number of years below the normal as an integer.
        """

        return metrics.get_years_compared_to_given_rainfall_value(
            self.get_yearly_rainfall(begin_year, end_year),
            metrics.get_normal(self.data, normal_year),
            opr.lt
        )

    def get_years_above_normal(self,
                               normal_year: int,
                               begin_year: int,
                               end_year: Optional[int] = None) -> int:
        """
        Computes the number of years above normal for a specific year range.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: The number of years above the normal as an integer.
        """

        return metrics.get_years_compared_to_given_rainfall_value(
            self.get_yearly_rainfall(begin_year, end_year),
            metrics.get_normal(self.data, normal_year),
            opr.gt
        )

    def get_last_year(self) -> int:
        """
        Retrieves the last element of the 'Year' column from the pandas DataFrame.

        :return: The ultimate year of DataFrame.
        """

        return int(self.data[Label.YEAR].iloc[-1])

    def get_relative_distance_from_normal(self,
                                          normal_year: int,
                                          begin_year: int,
                                          end_year: Optional[int] = None) -> float:
        """
        Computes the relative distance between above and below normal years
        for a specific year range.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :return: The relative distance as a float.
        """
        if end_year is None:
            end_year = self.get_last_year()

        gap: int = end_year - begin_year + 1
        if gap == 0:
            return 0.

        n_years_above_normal: int = self.get_years_above_normal(normal_year, begin_year, end_year)
        n_years_below_normal: int = self.get_years_below_normal(normal_year, begin_year, end_year)

        return round((n_years_above_normal - n_years_below_normal) / gap * 100,
                     self.round_precision)

    def get_standard_deviation(self,
                               begin_year: int,
                               end_year: Optional[int] = None,
                               label: Optional[Label] = Label.RAINFALL) -> Union[float, None]:
        """
        Compute the standard deviation of a column specified by its label within DataFrame
        and for an optional time range.
        By default, it uses the 'Rainfall' column.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values (optional).
        :param label: A string corresponding to an existing column label (optional).
        :return: The standard deviation as a float.
        Nothing if the specified column does not exist.
        """
        if label not in self.data.columns:
            return None

        return round(self.get_yearly_rainfall(begin_year, end_year)[label].std(),
                     self.round_precision)

    def add_percentage_of_normal(self,
                                 begin_year: int,
                                 end_year: Optional[int] = None) -> None:
        """
        Add the percentage of rainfall compared with normal
        to our pandas DataFrame for a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
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
            round(reg.coef_[0], self.round_precision)

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

        :param kmeans_clusters: The number of clusters to compute. Defaults to 4. (optional)
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

        return df_opr.remove_column(self.data, label)

    @plots.legend()
    def plot_rainfall(self) -> bool:
        """
        Plot Rainfall data according to year.

        :return: A boolean set to True if data has been successfully plotted, False otherwise.
        """

        success: bool = plotting.bar_column_according_to_year(self.data, Label.RAINFALL)
        if not success:
            return False

        return True

    @plots.legend()
    def plot_linear_regression(self) -> bool:
        """
        Plot linear regression of Rainfall data according to year.

        :return: A boolean set to True if data has been successfully plotted, False otherwise.
        """

        success: bool = plotting.plot_column_according_to_year(self.data,
                                                               Label.LINEAR_REGRESSION,
                                                               'red')
        if not success:
            return False

        return True

    @plots.legend()
    def plot_savgol_filter(self) -> bool:
        """
        Plot Savitzky–Golay filter of Rainfall data according to year.

        :return: A boolean set to True if data has been successfully plotted, False otherwise.
        """

        success: bool = plotting.plot_column_according_to_year(self.data,
                                                               Label.SAVITZKY_GOLAY_FILTER,
                                                               'orange')
        if not success:
            return False

        return True

    @plots.legend(ylabel=Label.PERCENTAGE_OF_NORMAL.value)
    def plot_normal(self, display_clusters: Optional[bool] = False) -> bool:
        """
        Plot Rainfall normals data according to year.

        :param display_clusters: The number of clusters to display
        :return: A boolean set to True if data has been successfully plotted, False otherwise.
        """
        plt.axhline(y=100.0, color='orange', linestyle='dashed', label='Normal')

        success: bool = False
        if not display_clusters:
            success = plotting.scatter_column_according_to_year(self.data,
                                                                Label.PERCENTAGE_OF_NORMAL)
        else:
            for label_value in range(metrics.get_clusters_number(self.data)):
                success = plotting.scatter_column_according_to_year(
                    self.data[self.data[Label.KMEANS.value] == label_value],
                    Label.PERCENTAGE_OF_NORMAL,
                    display_label=False
                )

                if not success:
                    return False

        if not success:
            return False

        return True
