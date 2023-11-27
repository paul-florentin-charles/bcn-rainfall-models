from src.core.utils.functions import plotting
from src.core.utils.enums.labels import Label

from tst.core.models.test_yearly_rainfall import yearly_rainfall, all_rainfall


class TestPlotting:
    @staticmethod
    def test_plot_column_according_to_year():
        is_plotted: bool = plotting.plot_column_according_to_year(
            yearly_rainfall.data, Label.RAINFALL
        )

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_scatter_column_according_to_year():
        is_plotted: bool = plotting.scatter_column_according_to_year(
            yearly_rainfall.data, Label.RAINFALL
        )

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_bar_column_according_to_year():
        is_plotted: bool = plotting.bar_column_according_to_year(
            yearly_rainfall.data, Label.RAINFALL
        )

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_bar_monthly_rainfall_averages():
        averages: list = plotting.bar_monthly_rainfall_averages(
            all_rainfall.monthly_rainfalls
        )

        assert isinstance(averages, list)
        assert len(averages) == len(all_rainfall.monthly_rainfalls)
        for average in averages:
            assert isinstance(average, float)

    @staticmethod
    def test_bar_monthly_rainfall_linreg_slopes():
        slopes: list = plotting.bar_monthly_rainfall_linreg_slopes(
            all_rainfall.monthly_rainfalls
        )

        assert isinstance(slopes, list)
        assert len(slopes) == len(all_rainfall.monthly_rainfalls)
        for slope in slopes:
            assert isinstance(slope, float)

    @staticmethod
    def test_bar_seasonal_rainfall_averages():
        averages: list = plotting.bar_seasonal_rainfall_averages(
            all_rainfall.seasonal_rainfalls
        )

        assert isinstance(averages, list)
        assert len(averages) == len(all_rainfall.seasonal_rainfalls)
        for average in averages:
            assert isinstance(average, float)

    @staticmethod
    def test_bar_seasonal_rainfall_linreg_slopes():
        slopes: list = plotting.bar_seasonal_rainfall_linreg_slopes(
            all_rainfall.seasonal_rainfalls
        )

        assert isinstance(slopes, list)
        assert len(slopes) == len(all_rainfall.seasonal_rainfalls)
        for slope in slopes:
            assert isinstance(slope, float)
