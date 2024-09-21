from src.core.utils.enums.labels import Label
from src.core.utils.functions import plotting
from tst.core.models.test_all_rainfall import begin_year, end_year
from tst.core.models.test_yearly_rainfall import YEARLY_RAINFALL, ALL_RAINFALL

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
    def test_bar_column_according_to_year():
        is_plotted = plotting.bar_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL
        )

        assert isinstance(is_plotted, bool)
        assert is_plotted

    @staticmethod
    def test_bar_monthly_rainfall_averages():
        averages = plotting.bar_monthly_rainfall_averages(
            ALL_RAINFALL.monthly_rainfalls.values(),
            begin_year=BEGIN_YEAR,
        )

        assert isinstance(averages, list)
        assert len(averages) == len(ALL_RAINFALL.monthly_rainfalls.values())
        for average in averages:
            assert isinstance(average, float)

    @staticmethod
    def test_bar_monthly_rainfall_linreg_slopes():
        slopes = plotting.bar_monthly_rainfall_linreg_slopes(
            list(ALL_RAINFALL.monthly_rainfalls.values()),
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(slopes, list)
        assert len(slopes) == len(ALL_RAINFALL.monthly_rainfalls)
        for slope in slopes:
            assert isinstance(slope, float)

    @staticmethod
    def test_bar_seasonal_rainfall_averages():
        averages = plotting.bar_seasonal_rainfall_averages(
            ALL_RAINFALL.seasonal_rainfalls.values(),
            begin_year=BEGIN_YEAR,
        )

        assert isinstance(averages, list)
        assert len(averages) == len(ALL_RAINFALL.seasonal_rainfalls)
        for average in averages:
            assert isinstance(average, float)

    @staticmethod
    def test_bar_seasonal_rainfall_linreg_slopes():
        slopes = plotting.bar_seasonal_rainfall_linreg_slopes(
            list(ALL_RAINFALL.seasonal_rainfalls.values()),
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(slopes, list)
        assert len(slopes) == len(ALL_RAINFALL.seasonal_rainfalls)
        for slope in slopes:
            assert isinstance(slope, float)
