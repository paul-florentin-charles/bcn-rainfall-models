from pytest import fixture, raises
from yaml.parser import ParserError  # type: ignore

from config import APISettings, Config, WebappServerSettings

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
        assert isinstance(config.get_data_settings.file_url, str)

    @staticmethod
    def test_get_dataset_path():
        assert isinstance(config.get_data_settings.local_file_path, str)

    @staticmethod
    def test_get_start_year():
        assert isinstance(config.get_data_settings.start_year, int)

    @staticmethod
    def test_get_rainfall_precision():
        assert isinstance(config.get_data_settings.rainfall_precision, int)

    @staticmethod
    def test_get_api_server_settings():
        api_server_settings = config.get_api_settings.server

        assert isinstance(api_server_settings, APISettings.APIServerSettings)
        assert api_server_settings.model_fields.keys() == {
            "host",
            "port",
            "reload",
        }

    @staticmethod
    def test_get_webapp_server_settings():
        assert isinstance(config.get_webapp_server_settings, WebappServerSettings)
        assert config.get_webapp_server_settings.model_fields.keys() == {
            "host",
            "port",
            "debug",
        }
