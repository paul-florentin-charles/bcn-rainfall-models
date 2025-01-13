import pandas as pd
import plotly.graph_objs as go

from back.rainfall.utils import Label, TimeMode, plotly_figures as plot
from tst.back.rainfall.models.test_all_rainfall import begin_year, end_year, normal_year
from tst.back.rainfall.models.test_yearly_rainfall import YEARLY_RAINFALL, ALL_RAINFALL


class TestPlotting:
    @staticmethod
    def test_get_figure_of_column_according_to_year():
        bar_fig = plot.get_figure_of_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL
        )

        assert isinstance(bar_fig, go.Figure)

        bar_fig = plot.get_figure_of_column_according_to_year(
            pd.DataFrame(), Label.RAINFALL
        )

        assert bar_fig is None

        scatter_fig = plot.get_figure_of_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL, figure_type="scatter"
        )

        assert isinstance(scatter_fig, go.Figure)

    @staticmethod
    def test_get_bar_figure_of_rainfall_averages():
        figure = plot.get_bar_figure_of_rainfall_averages(
            ALL_RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plot.get_bar_figure_of_rainfall_averages(
            ALL_RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

    @staticmethod
    def test_get_bar_figure_of_rainfall_linreg_slopes():
        figure = plot.get_bar_figure_of_rainfall_linreg_slopes(
            ALL_RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plot.get_bar_figure_of_rainfall_linreg_slopes(
            ALL_RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

    @staticmethod
    def test_get_bar_figure_of_relative_distances_to_normal():
        figure = plot.get_bar_figure_of_relative_distances_to_normal(
            ALL_RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plot.get_bar_figure_of_relative_distances_to_normal(
            ALL_RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)
