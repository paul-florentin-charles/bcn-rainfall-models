"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from functools import cached_property
from typing import Optional

from api_session import JSONDict
from pydantic import BaseModel, Field
from yaml import parser, safe_load  # type: ignore


class ServerSettings(BaseModel):
    """Base type definition for server settings"""

    host: str
    port: int


class APIServerSettings(ServerSettings):
    """Type definition for Uvicorn server settings."""

    reload: bool | None = Field(None)


class WebappServerSettings(ServerSettings):
    """Type definition for Flask server settings."""

    debug: bool | None = Field(None)


class FastAPISettings(BaseModel):
    """Type definition for FastAPI settings."""

    root_path: str
    title: str
    summary: str | None = Field(None)
    debug: bool | None = Field(None)


class DatasetSettings(BaseModel):
    """Type definition for dataset settings."""

    file_url: str
    local_file_path: str | None = Field(None)


class DataSettings(BaseModel):
    """Type definition for data settings."""

    start_year: int
    rainfall_precision: int
    kmeans_clusters: int | None = Field(None)


class Config:
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance: Optional["Config"] = None
    path: str
    yaml_config: JSONDict

    def __new__(cls, path="config.yml"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.path = path
            cls._instance._load_config()

        return cls._instance

    def _load_config(self):
        """Load and validate the configuration file."""
        try:
            with open(self.path, encoding="utf-8") as stream:
                self.yaml_config: JSONDict = safe_load(stream)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f'Configuration file not found at "{self.path}"'
            ) from exc
        except parser.ParserError as exc:
            raise parser.ParserError(
                f'Configuration file at "{self.path}" cannot be parsed: not a valid YAML file!'
            ) from exc

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
        Return the URL pointing to the CSV dataset.

        :return: The dataset URL as a String.
        """
        return DatasetSettings(**self.yaml_config["dataset"]).file_url

    @cached_property
    def get_dataset_path(self) -> str | None:
        """
        Return the path to the local copy of the CSV dataset.

        :return: The dataset path as a string.
        """
        return DatasetSettings(**self.yaml_config["dataset"]).local_file_path

    @cached_property
    def get_start_year(self) -> int:
        """
        Retrieve the year the data should start at.

        :return: A year as an Integer.
        """
        return DataSettings(**self.yaml_config["data"]).start_year

    @cached_property
    def get_rainfall_precision(self) -> int:
        """
        The decimal precision of Rainfall values.

        :return: A rounding precision as an Integer.
        """
        return DataSettings(**self.yaml_config["data"]).rainfall_precision

    @cached_property
    def get_api_server_settings(self) -> APIServerSettings:
        """
        Return Uvicorn server settings to run FastAPI app.

        :return: A dictionary containing server settings with typed keys.

        Example:
        {
            "host": "127.0.0.1",
            "port": 8000,
            "reload": True,
        }
        """
        return APIServerSettings(**self.yaml_config["api"]["server"])

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
        return FastAPISettings(**self.yaml_config["api"]["fastapi"])

    @cached_property
    def get_webapp_server_settings(self) -> WebappServerSettings:
        """
        Return Flask server settings.

        :return: A dictionary containing server settings with typed keys.

        Example:
        {
            "host": "127.0.0.1",
            "port": 5000,
            "debug": True,
        }
        """
        return WebappServerSettings(**self.yaml_config["webapp"])
