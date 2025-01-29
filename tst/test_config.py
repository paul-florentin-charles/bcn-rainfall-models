from pytest import fixture, raises
from yaml.parser import ParserError  # type: ignore

from config import Config

config = Config()


@fixture(autouse=True)
def reset_config():
    Config._instance = None
    yield


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
        assert isinstance(config.get_dataset_url, str)

    @staticmethod
    def test_get_start_year():
        assert isinstance(config.get_start_year, int)

    @staticmethod
    def test_get_rainfall_precision():
        assert isinstance(config.get_rainfall_precision, int)

    @staticmethod
    def test_get_kmeans_clusters():
        assert isinstance(config.get_kmeans_clusters, int)

    @staticmethod
    def test_get_api_server_settings():
        assert isinstance(config.get_api_server_settings, dict)
        assert config.get_api_server_settings.keys() == {"host", "port", "reload"}

    @staticmethod
    def test_get_webapp_server_settings():
        assert isinstance(config.get_webapp_server_settings, dict)
        assert config.get_webapp_server_settings.keys() == {"host", "port", "debug"}
