import pandas as pd
from plotly.graph_objs import Figure

from back.core.utils.enums import TimeMode
from back.core.utils.enums.labels import Label
from back.core.utils.functions import plotting
from tst.back.core.models.test_all_rainfall import begin_year, end_year, normal_year
from tst.back.core.models.test_yearly_rainfall import YEARLY_RAINFALL, ALL_RAINFALL


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
    def test_get_bar_figure_of_rainfall_averages():
        figure = plotting.get_bar_figure_of_rainfall_averages(
            ALL_RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)

        figure = plotting.get_bar_figure_of_rainfall_averages(
            ALL_RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)

    @staticmethod
    def test_get_bar_figure_of_rainfall_linreg_slopes():
        figure = plotting.get_bar_figure_of_rainfall_linreg_slopes(
            ALL_RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)

        figure = plotting.get_bar_figure_of_rainfall_linreg_slopes(
            ALL_RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)

    @staticmethod
    def test_get_bar_figure_of_relative_distances_to_normal():
        figure = plotting.get_bar_figure_of_relative_distances_to_normal(
            ALL_RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)

        figure = plotting.get_bar_figure_of_relative_distances_to_normal(
            ALL_RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, Figure)
