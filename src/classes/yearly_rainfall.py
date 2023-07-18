import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from typing import Optional


class YearlyRainfall:
    dataset_url: str = str.format(
        "https://opendata-ajuntament.barcelona.cat/data/dataset/{0}/resource/{1}/download/{2}",
        "5334c15e-0d70-410b-85f3-d97740ffc1ed",
        "6f1fb778-0767-478b-b332-c64a833d26d2",
        "precipitacionsbarcelonadesde1786.csv"
    )

    def __init__(self, __starting_year):
        self.__starting_year = __starting_year
        self.__yearly_rainfall: pd.DataFrame = YearlyRainfall.load_yearly_rainfall(self.__starting_year)

    def __str__(self):
        return self.__yearly_rainfall.to_string()

    def get_yearly_rainfall(self):
        return self.__yearly_rainfall

    def get_starting_year(self):
        return self.__starting_year

    def export_as_csv(self, path: Optional[str] = None) -> str:
        return self.__yearly_rainfall.to_csv(path_or_buf=path, index=False)

    def get_average_yearly_rainfall(self,
                                    begin_year: Optional[int] = None,
                                    end_year: Optional[int] = None) -> float:
        yr: pd.DataFrame = self.__yearly_rainfall.copy(deep=True)

        if begin_year is not None:
            yr = yr[yr['Year'] >= begin_year]

        if end_year is not None:
            yr = yr[yr['Year'] <= end_year]

        nb_years: int = len(yr)
        if nb_years == 0:
            return 0.

        yr = yr.sum(axis='rows')

        return round(yr.loc['Rainfall'] / nb_years, 2)

    def get_years_below_average(self,
                                begin_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> int:
        average_yearly_rainfall = self.get_average_yearly_rainfall(begin_year, end_year)

        yr = self.__yearly_rainfall[self.__yearly_rainfall['Rainfall'] < average_yearly_rainfall]

        return yr.count()['Year']

    def get_years_above_average(self,
                                begin_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> int:
        average_yearly_rainfall = self.get_average_yearly_rainfall(begin_year, end_year)

        yr = self.__yearly_rainfall[self.__yearly_rainfall['Rainfall'] > average_yearly_rainfall]

        return yr.count()['Year']

    def add_percentage_of_normal(self,
                                 begin_year: Optional[int] = None,
                                 end_year: Optional[int] = None) -> None:
        normal: float = self.get_average_yearly_rainfall(begin_year, end_year)
        if normal == 0.:
            return

        self.__yearly_rainfall['Percentage of normal'] = round(self.__yearly_rainfall['Rainfall'] / normal * 100.0, 2)

    def add_linear_regression(self) -> (float, float):
        years: np.ndarray = self.__yearly_rainfall['Year'].values.reshape(-1, 1)
        rainfalls: np.ndarray = self.__yearly_rainfall['Rainfall'].values

        reg = LinearRegression()
        reg.fit(years, rainfalls)
        self.__yearly_rainfall['LinReg'] = reg.predict(years)
        self.__yearly_rainfall['LinReg'] = round(self.__yearly_rainfall['LinReg'], 2)

        return r2_score(rainfalls,
                        self.__yearly_rainfall['LinReg'].values), \
            reg.coef_[0]

    @classmethod
    def load_yearly_rainfall(cls, starting_year) -> pd.DataFrame:
        monthly_rainfall: pd.DataFrame = pd.read_csv(cls.dataset_url)

        years: pd.DataFrame = monthly_rainfall.iloc[:, :1]
        rainfall: pd.Series = monthly_rainfall.iloc[:, 1:].sum(axis='columns')

        yearly_rainfall: pd.DataFrame = pd.concat((years, rainfall), axis='columns') \
            .set_axis(['Year', 'Rainfall'],
                      axis='columns')
        yearly_rainfall = yearly_rainfall[yearly_rainfall['Year'] >= starting_year] \
            .reset_index() \
            .drop(columns='index')

        yearly_rainfall['Rainfall'] = round(yearly_rainfall['Rainfall'], 2)

        return yearly_rainfall
