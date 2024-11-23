from pytest import raises
from yaml.parser import ParserError  # type: ignore

from config import Config, CONFIG_FNAME

config: Config = Config(path=CONFIG_FNAME)


class TestConfig:
    @staticmethod
    def test_config_file_not_found():
        with raises(FileNotFoundError):
            Config(path="/there/is/no/config/file/there/dude.yaml")

    @staticmethod
    def test_config_file_invalid():
        with raises(ParserError):
            Config(path="README.md")

    @staticmethod
    def test_get_dataset_url():
        dataset_url = config.get_dataset_url()
        assert isinstance(dataset_url, str)

    @staticmethod
    def test_get_start_year():
        start_year = config.get_start_year()
        assert isinstance(start_year, int)

    @staticmethod
    def test_get_rainfall_precision():
        rainfall_precision = config.get_rainfall_precision()
        assert isinstance(rainfall_precision, int)

    @staticmethod
    def test_get_kmeans_clusters():
        kmeans_clusters = config.get_kmeans_clusters()
        assert isinstance(kmeans_clusters, int)

    @staticmethod
    def test_get_api_server_settings():
        settings = config.get_api_server_settings()
        assert isinstance(settings, dict)
        assert settings.keys() == {"host", "port", "reload"}

    @staticmethod
    def test_get_webapp_server_settings():
        settings = config.get_webapp_server_settings()
        assert isinstance(settings, dict)
        assert settings.keys() == {"host", "port", "debug"}
