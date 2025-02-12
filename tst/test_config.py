from pytest import fixture, raises
from yaml.parser import ParserError  # type: ignore

from back.api.config import APISettings
from back.api.config import Config as APIConfig
from back.rainfall.config import Config as RainfallConfig
from base_config import BaseConfig
from webapp.config import Config as WebappConfig
from webapp.config import WebappServerSettings


@fixture(autouse=True)
def reset_config():
    for config in [BaseConfig, RainfallConfig, APIConfig, WebappConfig]:  # type: ignore
        config._instance = None

    yield


class TestConfig:
    @staticmethod
    def test_config_file_not_found():
        with raises(FileNotFoundError):
            BaseConfig(path="/there/is/no/config/file/there/dude.yaml")

    @staticmethod
    def test_config_file_invalid():
        with raises(ParserError):
            BaseConfig(path="README.md")

    @staticmethod
    def test_get_data_settings():
        data_settings = RainfallConfig().get_data_settings

        assert isinstance(data_settings.file_url, str)

        if data_settings.local_file_path is not None:
            assert isinstance(data_settings.local_file_path, str)

        assert isinstance(data_settings.start_year, int)
        assert isinstance(data_settings.rainfall_precision, int)

    @staticmethod
    def test_get_api_server_settings():
        api_server_settings = APIConfig().get_api_settings.server

        assert isinstance(api_server_settings, APISettings.APIServerSettings)
        assert api_server_settings.model_fields.keys() == {
            "host",
            "port",
            "reload",
        }

    @staticmethod
    def test_get_webapp_server_settings():
        webapp_server_settings = WebappConfig().get_webapp_server_settings

        assert isinstance(webapp_server_settings, WebappServerSettings)
        assert webapp_server_settings.model_fields.keys() == {
            "host",
            "port",
            "debug",
        }
