# pylint: disable=missing-docstring

from operator import lt

from src.core.utils.functions import metrics
from src.core.utils.enums.labels import Label

from tst.core.models.test_yearly_rainfall import yearly_rainfall


class TestMetrics:
    @staticmethod
    def test_get_average_rainfall() -> None:
        precision: int = 3
        avg_rainfall: float = metrics.get_average_rainfall(
            yearly_rainfall.data, precision
        )

        assert isinstance(avg_rainfall, float)
        assert len(str(avg_rainfall).split(".")[1]) <= precision

    @staticmethod
    def test_get_years_compared_to_given_rainfall_value() -> None:
        nb_years: int = metrics.get_years_compared_to_given_rainfall_value(
            yearly_rainfall.data, metrics.get_average_rainfall(yearly_rainfall.data), lt
        )

        assert nb_years <= len(yearly_rainfall.data)

    @staticmethod
    def test_get_clusters_number() -> None:
        nb_clusters: int = metrics.get_clusters_number(yearly_rainfall.data)

        if Label.KMEANS not in yearly_rainfall.data:
            assert nb_clusters == 0
        else:
            assert nb_clusters > 0

    @staticmethod
    def test_get_normal() -> None:
        normal: float = metrics.get_normal(yearly_rainfall.data, begin_year=1991)

        assert isinstance(normal, float)
        assert normal >= 0.0
