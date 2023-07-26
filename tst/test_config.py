# pylint: disable=missing-docstring

from src.config import Config, CONFIG_FILE_PATH

cfg: Config = Config(f"src/{CONFIG_FILE_PATH}")


class TestConfig:
    @staticmethod
    def test_get_dataset_url() -> None:
        dataset_url: str = cfg.get_dataset_url()
        assert isinstance(dataset_url, str)

    @staticmethod
    def test_get_start_year() -> None:
        start_year: int = cfg.get_start_year()
        assert isinstance(start_year, int)

    @staticmethod
    def test_get_rainfall_precision() -> None:
        rainfall_precision: int = cfg.get_rainfall_precision()
        assert isinstance(rainfall_precision, int)

    @staticmethod
    def test_get_kmeans_clusters() -> None:
        kmeans_clusters: int = cfg.get_kmeans_clusters()
        assert isinstance(kmeans_clusters, int)
