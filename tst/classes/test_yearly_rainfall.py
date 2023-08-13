# pylint: disable=missing-docstring

import matplotlib.pyplot as plt
import pandas as pd

from src.classes.yearly_rainfall import YearlyRainfall
from src.enums.labels import Label
from src.enums.months import Month
from tst.test_config import config

yearly_rainfall = YearlyRainfall(config.get_dataset_url())


class TestYearlyRainfall:
    @staticmethod
    def test_load_yearly_rainfall() -> None:
        data: pd.DataFrame = yearly_rainfall.load_yearly_rainfall()

        assert isinstance(data, pd.DataFrame)

    @staticmethod
    def test_load_rainfall() -> None:
        data: pd.DataFrame = yearly_rainfall.load_rainfall(start_month=Month.JUNE.value,
                                                           end_month=Month.OCTOBER.value)
        assert isinstance(data, pd.DataFrame)
        assert len(data.columns) == 2
        assert Label.YEAR in data \
               and Label.RAINFALL in data

    @staticmethod
    def test_get_yearly_rainfall() -> None:
        begin_year: int = 1970
        end_year: int = 2010
        data: pd.DataFrame = yearly_rainfall.get_yearly_rainfall(begin_year, end_year)

        assert isinstance(data, pd.DataFrame)
        assert len(data) == end_year - begin_year + 1

    @staticmethod
    def test_export_as_csv() -> None:
        csv_as_str: str = yearly_rainfall.export_as_csv()

        assert isinstance(csv_as_str, str)

    @staticmethod
    def test_get_average_yearly_rainfall() -> None:
        begin_year: int = 1980
        end_year: int = 2005
        avg_rainfall: float = yearly_rainfall.get_average_yearly_rainfall(begin_year, end_year)

        assert isinstance(avg_rainfall, float)

    @staticmethod
    def test_get_years_below_average() -> None:
        begin_year: int = 1950
        end_year: int = 1975
        n_years_below_avg: int = yearly_rainfall.get_years_below_average(begin_year, end_year)

        assert isinstance(n_years_below_avg, int)
        assert n_years_below_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_above_average() -> None:
        begin_year: int = 1950
        end_year: int = 1975
        n_years_above_avg: int = yearly_rainfall.get_years_above_average(begin_year, end_year)

        assert isinstance(n_years_above_avg, int)
        assert n_years_above_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_standard_deviation() -> None:
        std: float = yearly_rainfall.get_standard_deviation()

        assert isinstance(std, float)

        std = yearly_rainfall.get_standard_deviation(label=Label.SAVITZKY_GOLAY_FILTER)

        assert std is None

    @staticmethod
    def test_add_percentage_of_normal() -> None:
        yearly_rainfall.add_percentage_of_normal()

        assert Label.PERCENTAGE_OF_NORMAL in yearly_rainfall.data

    @staticmethod
    def test_add_linear_regression() -> None:
        yearly_rainfall.add_linear_regression()

        assert Label.LINEAR_REGRESSION in yearly_rainfall.data

    @staticmethod
    def test_add_savgol_filter() -> None:
        yearly_rainfall.add_savgol_filter()

        assert Label.SAVITZKY_GOLAY_FILTER in yearly_rainfall.data

    @staticmethod
    def test_add_kmeans() -> None:
        kmeans_clusters: int = 5
        n_clusters: int = yearly_rainfall.add_kmeans(kmeans_clusters)

        assert n_clusters == kmeans_clusters
        assert Label.KMEANS in yearly_rainfall.data

    @staticmethod
    def test_remove_column() -> None:
        removed: bool = yearly_rainfall.remove_column(Label.YEAR)

        assert not removed

        removed = yearly_rainfall.remove_column(Label.SAVITZKY_GOLAY_FILTER)
        yearly_rainfall.add_savgol_filter()

        assert removed

    @staticmethod
    def test_plot_rainfall_and_models() -> None:
        yearly_rainfall.plot_rainfall()
        yearly_rainfall.plot_linear_regression()
        yearly_rainfall.plot_savgol_filter()
        plt.show()

    @staticmethod
    def test_plot_normal() -> None:
        yearly_rainfall.plot_normal()
        plt.show()
