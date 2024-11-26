from operator import lt

from back.core.utils.enums.labels import Label
from back.core.utils.functions import metrics
from tst.back.core.models.test_yearly_rainfall import YEARLY_RAINFALL


class TestMetrics:
    @staticmethod
    def test_get_average_rainfall():
        precision = 3
        avg_rainfall = metrics.get_average_rainfall(
            YEARLY_RAINFALL.data, round_precision=precision
        )

        assert isinstance(avg_rainfall, float)
        assert len(str(avg_rainfall).split(".")[1]) <= precision

    @staticmethod
    def test_get_years_compared_to_given_rainfall_value():
        nb_years = metrics.get_years_compared_to_given_rainfall_value(
            YEARLY_RAINFALL.data,
            metrics.get_average_rainfall(YEARLY_RAINFALL.data),
            comparator=lt,
        )

        assert nb_years <= len(YEARLY_RAINFALL.data)

    @staticmethod
    def test_get_clusters_number():
        nb_clusters = metrics.get_clusters_number(YEARLY_RAINFALL.data)

        if Label.KMEANS not in YEARLY_RAINFALL.data:
            assert nb_clusters == 0
        else:
            assert nb_clusters > 0

    @staticmethod
    def test_get_normal():
        normal = metrics.get_normal(YEARLY_RAINFALL.data, begin_year=1991)

        assert isinstance(normal, float)
        assert normal >= 0.0
