"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from functools import cached_property
from typing import Any, TypedDict, NotRequired

from yaml import parser, safe_load  # type: ignore


class ServerSettings(TypedDict):
    """Type definition for server settings (both API and Webapp)."""

    host: str
    port: int


class FastAPISettings(TypedDict):
    """Type definition for FastAPI settings."""

    debug: NotRequired[bool]
    root_path: str
    title: str
    summary: NotRequired[str]


class Config:
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance = None
    path: str
    yaml_config: dict[str, Any]

    def __new__(cls, path="config.yml"):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.path = path
            cls._instance._load_config()

        return cls._instance

    def _load_config(self):
        """Load and validate the configuration file."""
        try:
            with open(self.path, mode="rt", encoding="utf-8") as stream:
                self.yaml_config: dict[str, Any] = safe_load(stream)

            self._validate_config()
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f'Configuration file not found at "{self.path}"'
            ) from exc
        except parser.ParserError as exc:
            raise parser.ParserError(
                f'Configuration file at "{self.path}" cannot be parsed: not a valid YAML file!'
            ) from exc

    def _validate_config(self):
        """Validate the configuration structure."""
        required_keys = {
            "dataset": {"file_url", "local_file_path"},
            "data": {"start_year", "rainfall_precision", "kmeans_clusters"},
            "api": {"server", "fastapi"},
            "webapp": {"host", "port"},
        }

        for section, fields in required_keys.items():
            if section not in self.yaml_config:
                raise ValueError(f"Missing required section: {section}")
            for field in fields:
                if field not in self.yaml_config[section]:
                    raise ValueError(f"Missing required field: {section}.{field}")

    @classmethod
    def reload(cls):
        """
        Reload the configuration from the file.
        This is a class method since we're using the Singleton pattern.
        """
        if cls._instance is not None:
            cls._instance._load_config()
        else:
            raise RuntimeError(
                "Cannot reload configuration: no instance has been created yet."
            )

    @cached_property
    def get_dataset_url(self) -> str:
        """
        Build the dataset URL location from the configuration.

        :return: The dataset URL as a String.
        """
        return self.yaml_config["dataset"]["file_url"]

    @cached_property
    def get_dataset_path(self) -> str:
        """
        Return the path to the local copy of the dataset.

        :return: The dataset path as a string.
        """
        return self.yaml_config["dataset"]["local_file_path"]

    @cached_property
    def get_start_year(self) -> int:
        """
        Retrieve the year the data should start at.

        :return: A year as an Integer.
        """
        return self.yaml_config["data"]["start_year"]

    @cached_property
    def get_rainfall_precision(self) -> int:
        """
        The decimal precision of Rainfall values.

        :return: A rounding precision as an Integer.
        """
        return self.yaml_config["data"]["rainfall_precision"]

    @cached_property
    def get_kmeans_clusters(self) -> int:
        """
        The number of clusters to use for K-Means clustering of Rainfall data.

        :return: A number of clusters as an Integer.
        """
        return self.yaml_config["data"]["kmeans_clusters"]

    @cached_property
    def get_api_server_settings(self) -> ServerSettings:
        """
        Return Uvicorn server settings to run FastAPI app.

        :return: A dictionary containing server settings with typed keys.

        Example:
        {
            "host": "127.0.0.1",
            "port": 8000,
        }
        """
        return self.yaml_config["api"]["server"]

    @cached_property
    def get_fastapi_settings(self) -> FastAPISettings:
        """
        Return FastAPI settings to initiate app.

        :return: A dictionary containing FastAPI settings with typed keys.

        Example:
        {
            "debug": True,
            "root_path": "/api",
            "title": "Barcelona Rainfall API",
            "summary": "An API that provides rainfall-related data of the city of Barcelona."
        }
        """
        return self.yaml_config["api"]["fastapi"]

    @cached_property
    def get_webapp_server_settings(self) -> ServerSettings:
        """
        Return Flask server settings.

        :return: A dictionary containing server settings with typed keys.

        Example:
        {
            "host": "127.0.0.1",
            "port": 5000
        }
        """
        return self.yaml_config["webapp"]
