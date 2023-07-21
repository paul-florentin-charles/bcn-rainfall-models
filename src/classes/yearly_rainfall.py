import pandas as pd
import numpy as np
from scipy import signal
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

from typing import Optional

YEAR: str = 'Year'
RAINFALL: str = 'Rainfall'
PERCENTAGE_OF_NORMAL: str = 'Percentage of normal'
LINEAR_REGRESSION: str = 'Linear regression'
SAVITZKY_GOLAY_FILTER: str = 'Savitzky–Golay filter'


class YearlyRainfall:
    dataset_url: str = str.format(
        "https://opendata-ajuntament.barcelona.cat/data/dataset/{0}/resource/{1}/download/{2}",
        "5334c15e-0d70-410b-85f3-d97740ffc1ed",
        "6f1fb778-0767-478b-b332-c64a833d26d2",
        "precipitacionsbarcelonadesde1786.csv"
    )

    def __init__(self,
                 yearly_rainfall: Optional[pd.DataFrame] = None,
                 starting_year: Optional[int] = None):
        if yearly_rainfall is None:
            self.__yearly_rainfall: pd.DataFrame = YearlyRainfall.load_yearly_rainfall(starting_year)
        else:
            self.__yearly_rainfall: pd.DataFrame = yearly_rainfall
        self.__starting_year: int = starting_year

    def __str__(self):
        return self.__yearly_rainfall.to_string()

    def get_yearly_rainfall(self,
                            begin_year: Optional[int] = None,
                            end_year: Optional[int] = None) -> pd.DataFrame:
        yr: pd.DataFrame = self.__yearly_rainfall

        if begin_year is not None:
            yr = yr[yr[YEAR] >= begin_year]

        if end_year is not None:
            yr = yr[yr[YEAR] <= end_year]

        return yr

    def get_starting_year(self) -> int:
        return self.__starting_year

    def export_as_csv(self, path: Optional[str] = None) -> str:
        return self.__yearly_rainfall.to_csv(path_or_buf=path, index=False)

    def get_average_yearly_rainfall(self,
                                    begin_year: Optional[int] = None,
                                    end_year: Optional[int] = None) -> float:
        yr: pd.DataFrame = self.get_yearly_rainfall(begin_year, end_year)

        nb_years: int = len(yr)
        if nb_years == 0:
            return 0.

        yr = yr.sum(axis='rows')

        return round(yr.loc[RAINFALL] / nb_years, 2)

    def get_years_below_average(self,
                                begin_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> int:
        yr: pd.DataFrame = self.get_yearly_rainfall(begin_year, end_year)

        yr = yr[yr[RAINFALL] < self.get_average_yearly_rainfall(begin_year, end_year)]

        return yr.count()[YEAR]

    def get_years_above_average(self,
                                begin_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> int:
        yr: pd.DataFrame = self.get_yearly_rainfall(begin_year, end_year)

        yr = yr[yr[RAINFALL] > self.get_average_yearly_rainfall(begin_year, end_year)]

        return yr.count()[YEAR]

    def add_percentage_of_normal(self,
                                 begin_year: Optional[int] = None,
                                 end_year: Optional[int] = None) -> None:
        normal: float = self.get_average_yearly_rainfall(begin_year, end_year)
        if normal == 0.:
            return

        self.__yearly_rainfall[PERCENTAGE_OF_NORMAL] = round(self.__yearly_rainfall[RAINFALL] / normal * 100.0, 2)

    def add_linear_regression(self) -> (float, float):
        years: np.ndarray = self.__yearly_rainfall[YEAR].values.reshape(-1, 1)
        rainfalls: np.ndarray = self.__yearly_rainfall[RAINFALL].values

        reg = LinearRegression()
        reg.fit(years, rainfalls)
        self.__yearly_rainfall[LINEAR_REGRESSION] = reg.predict(years)
        self.__yearly_rainfall[LINEAR_REGRESSION] = round(self.__yearly_rainfall[LINEAR_REGRESSION], 2)

        return r2_score(rainfalls,
                        self.__yearly_rainfall[LINEAR_REGRESSION].values), \
            reg.coef_[0]

    def add_savgol_filter(self) -> None:
        self.__yearly_rainfall[SAVITZKY_GOLAY_FILTER] = signal.savgol_filter(self.__yearly_rainfall[RAINFALL],
                                                                             window_length=len(self.__yearly_rainfall),
                                                                             polyorder=len(
                                                                                 self.__yearly_rainfall) // 10)

        self.__yearly_rainfall[SAVITZKY_GOLAY_FILTER] = round(self.__yearly_rainfall[SAVITZKY_GOLAY_FILTER], 2)

    def plot_rainfall(self, show: Optional[bool] = False) -> None:
        for column_label in self.__yearly_rainfall.columns[1:]:
            if column_label == PERCENTAGE_OF_NORMAL:
                continue

            plt.plot(self.__yearly_rainfall[YEAR],
                     self.__yearly_rainfall[column_label],
                     label=column_label)

        plt.xlabel(YEAR)
        plt.ylabel(f"{RAINFALL} in (mm)")
        plt.title("Barcelona rainfall evolution and various models")
        plt.legend()
        if show:
            plt.show()

    def plot_normal(self, show: Optional[bool] = False) -> None:
        if PERCENTAGE_OF_NORMAL not in self.__yearly_rainfall.columns:
            return

        plt.axhline(y=100.0, color='orange', linestyle='dashed', label='Normal')
        plt.scatter(self.__yearly_rainfall[YEAR],
                    self.__yearly_rainfall[PERCENTAGE_OF_NORMAL],
                    label=PERCENTAGE_OF_NORMAL)

        plt.xlabel(YEAR)
        plt.ylabel("Percentage (%)")
        plt.title("Barcelona rainfall evolution compared to normal")
        plt.legend()
        if show:
            plt.show()

    @classmethod
    def load_yearly_rainfall(cls, starting_year: Optional[int] = None) -> pd.DataFrame:
        monthly_rainfall: pd.DataFrame = pd.read_csv(cls.dataset_url)

        years: pd.DataFrame = monthly_rainfall.iloc[:, :1]
        rainfall: pd.Series = monthly_rainfall.iloc[:, 1:].sum(axis='columns')

        yearly_rainfall: pd.DataFrame = pd.concat((years, rainfall), axis='columns') \
            .set_axis([YEAR, RAINFALL],
                      axis='columns')

        if starting_year is not None:
            yearly_rainfall = yearly_rainfall[yearly_rainfall[YEAR] >= starting_year] \
                .reset_index() \
                .drop(columns='index')

        yearly_rainfall[RAINFALL] = round(yearly_rainfall[RAINFALL], 2)

        return yearly_rainfall
