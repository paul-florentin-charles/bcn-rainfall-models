import pandas as pd
from plotly.graph_objs import Figure

from back.core.utils.enums.labels import Label
from back.core.utils.functions import plotting
from tst.back.core.models.test_all_rainfall import begin_year, end_year, normal_year
from tst.back.core.models.test_yearly_rainfall import YEARLY_RAINFALL, ALL_RAINFALL

BEGIN_YEAR = 1970


class TestPlotting:
    @staticmethod
    def test_plot_column_according_to_year():
        is_plotted = plotting.plot_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL
        )

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_scatter_column_according_to_year():
        is_plotted = plotting.scatter_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL
        )

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_get_bar_figure_of_column_according_to_year():
        bar_fig = plotting.get_bar_figure_of_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL
        )

        assert isinstance(bar_fig, Figure)

        bar_fig = plotting.get_bar_figure_of_column_according_to_year(
            pd.DataFrame(), Label.RAINFALL
        )

        assert bar_fig is None

    @staticmethod
    def test_get_bar_figure_of_monthly_rainfall_averages():
        figure = plotting.get_bar_figure_of_monthly_rainfall_averages(
            ALL_RAINFALL.monthly_rainfalls.values(),
            begin_year=BEGIN_YEAR,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)

    @staticmethod
    def test_bar_seasonal_rainfall_averages():
        figure = plotting.get_bar_figure_of_seasonal_rainfall_averages(
            ALL_RAINFALL.seasonal_rainfalls.values(),
            begin_year=BEGIN_YEAR,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)

    @staticmethod
    def test_bar_monthly_rainfall_linreg_slopes():
        slopes = plotting.get_bar_figure_of_monthly_rainfall_linreg_slopes(
            list(ALL_RAINFALL.monthly_rainfalls.values()),
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(slopes, Figure)

    @staticmethod
    def test_bar_seasonal_rainfall_linreg_slopes():
        slopes = plotting.get_bar_figure_of_seasonal_rainfall_linreg_slopes(
            list(ALL_RAINFALL.seasonal_rainfalls.values()),
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(slopes, Figure)

    @staticmethod
    def test_bar_monthly_relative_distances_to_normal():
        relative_distances_to_normal = (
            plotting.bar_monthly_relative_distances_to_normal(
                list(ALL_RAINFALL.monthly_rainfalls.values()),
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
            )
        )

        assert isinstance(relative_distances_to_normal, list)
        assert len(relative_distances_to_normal) == len(ALL_RAINFALL.monthly_rainfalls)
        for relative_distance_to_normal in relative_distances_to_normal:
            assert isinstance(relative_distance_to_normal, float)

    @staticmethod
    def test_bar_seasonal_relative_distances_to_normal():
        relative_distances_to_normal = (
            plotting.bar_seasonal_relative_distances_to_normal(
                list(ALL_RAINFALL.seasonal_rainfalls.values()),
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
            )
        )

        assert isinstance(relative_distances_to_normal, list)
        assert len(relative_distances_to_normal) == len(ALL_RAINFALL.seasonal_rainfalls)
        for relative_distance_to_normal in relative_distances_to_normal:
            assert isinstance(relative_distance_to_normal, float)
