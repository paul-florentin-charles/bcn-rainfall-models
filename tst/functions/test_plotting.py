# pylint: disable=missing-docstring

from src.core.utils.functions import plotting
from src.core.utils.enums.labels import Label

from tst.models.test_yearly_rainfall import yearly_rainfall


class TestPlotting:
    @staticmethod
    def test_plot_column_according_to_year():
        is_plotted: bool = plotting.plot_column_according_to_year(yearly_rainfall.data,
                                                                  Label.RAINFALL)

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_scatter_column_according_to_year():
        is_plotted: bool = plotting.scatter_column_according_to_year(yearly_rainfall.data,
                                                                     Label.RAINFALL)

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_bar_column_according_to_year():
        is_plotted: bool = plotting.bar_column_according_to_year(yearly_rainfall.data,
                                                                 Label.RAINFALL)

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_bar_monthly_rainfall_averages():
        pass

    @staticmethod
    def test_bar_monthly_rainfall_linreg_slopes():
        pass

    @staticmethod
    def test_bar_seasonal_rainfall_averages():
        pass

    @staticmethod
    def test_bar_seasonal_rainfall_linreg_slopes():
        pass
