from pytest import raises
from yaml.parser import ParserError

from src.config import Config, CONFIG_FNAME

config: Config = Config(path=CONFIG_FNAME)


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

    @staticmethod
    def test_config_file_not_found() -> None:
        with raises(FileNotFoundError):
            Config(path="/there/is/no/config/file/there/dude.yaml")

    @staticmethod
    def test_config_file_invalid() -> None:
        with raises(ParserError):
            Config(path="README.md")
