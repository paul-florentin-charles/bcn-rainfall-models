import pandas as pd

from typing import Optional


class YearlyRainfall:
    dataset_url: str = str.format(
        "https://opendata-ajuntament.barcelona.cat/data/dataset/{0}/resource/{1}/download/{2}",
        "5334c15e-0d70-410b-85f3-d97740ffc1ed",
        "6f1fb778-0767-478b-b332-c64a833d26d2",
        "precipitacionsbarcelonadesde1786.csv"
    )

    starting_year: int = 1970

    def __init__(self):
        self.yearly_rainfall: pd.DataFrame = YearlyRainfall.retrieve_yearly_rainfall()

    def __str__(self):
        return self.yearly_rainfall.to_string()

    def get_average_yearly_rainfall(self,
                                    begin_year: Optional[int] = None,
                                    end_year: Optional[int] = None) -> float:
        yr: pd.DataFrame = self.yearly_rainfall.copy(deep=True)

        if begin_year is not None:
            yr = yr[yr['Year'] >= begin_year]

        if end_year is not None:
            yr = yr[yr['Year'] <= end_year]

        nb_years: int = len(yr)
        if nb_years == 0:
            return 0.

        yr = yr.sum(axis='rows')

        return round(yr.loc['Rainfall'] / nb_years, 2)

    @classmethod
    def retrieve_yearly_rainfall(cls) -> pd.DataFrame:
        monthly_rainfall: pd.DataFrame = pd.read_csv(cls.dataset_url)

        years: pd.DataFrame = monthly_rainfall.iloc[:, :1]
        rainfall: pd.Series = monthly_rainfall.iloc[:, 1:].sum(axis='columns')

        yearly_rainfall: pd.DataFrame = pd.concat((years, rainfall), axis='columns') \
            .set_axis(['Year', 'Rainfall'],
                      axis='columns')
        yearly_rainfall = yearly_rainfall[yearly_rainfall['Year'] >= cls.starting_year] \
            .reset_index() \
            .drop(columns='index')

        return yearly_rainfall
