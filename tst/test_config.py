# pylint: disable=missing-docstring

from config import Config, CONFIG_FNAME

config: Config = Config(path=f"src/{CONFIG_FNAME}")


class TestConfig:
    @staticmethod
    def test_get_dataset_url() -> None:
        dataset_url: str = config.get_dataset_url()
        assert isinstance(dataset_url, str)

    @staticmethod
    def test_get_start_year() -> None:
        start_year: int = config.get_start_year()
        assert isinstance(start_year, int)

    @staticmethod
    def test_get_rainfall_precision() -> None:
        rainfall_precision: int = config.get_rainfall_precision()
        assert isinstance(rainfall_precision, int)

    @staticmethod
    def test_get_kmeans_clusters() -> None:
        kmeans_clusters: int = config.get_kmeans_clusters()
        assert isinstance(kmeans_clusters, int)
