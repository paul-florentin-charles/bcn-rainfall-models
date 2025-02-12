"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from functools import cached_property
from typing import Optional

from api_session import JSONDict
from pydantic import BaseModel, Field
from yaml import parser, safe_load  # type: ignore


class WebappServerSettings(BaseModel):
    """Type definition for Flask server settings."""

    host: str
    port: int
    debug: bool | None = Field(None)


class APISettings(BaseModel):
    """Type definition for API settings: FastAPI settings & Uvicorn server settings."""

    class FastAPISettings(BaseModel):
        """Type definition for FastAPI settings."""

        root_path: str
        title: str
        summary: str | None = Field(None)
        debug: bool | None = Field(None)

    class APIServerSettings(BaseModel):
        """Type definition for Uvicorn server settings."""

        host: str
        port: int
        reload: bool | None = Field(None)

    fastapi: FastAPISettings
    server: APIServerSettings


class DataSettings(BaseModel):
    """Type definition for data settings."""

    file_url: str
    local_file_path: str | None = Field(None)
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
    def get_data_settings(self) -> DataSettings:
        """
        Return data settings to load and manipulate rainfall data.

        Example:
        {
            "file_url": "https://opendata-ajuntament.barcelona.cat/data/dataset/5334c15e-0d70-410b-85f3-d97740ffc1ed/resource/6f1fb778-0767-478b-b332-c64a833d26d2/download/precipitacionsbarcelonadesde1786.csv",
            "local_file_path": "resources/bcn_rainfall_1786_2024.csv",
            "start_year": 1971,
            "rainfall_precision": 1,
        }
        """
        return DataSettings(**self.yaml_config["data"])

    @cached_property
    def get_api_settings(self) -> APISettings:
        """
        Return both FastAPI settings and Uvicorn server settings to run FastAPI app.

        Example:
        {
            "fastapi": {
                "debug": True,
                "root_path": "/api",
                "title": "Barcelona Rainfall API",
                "summary": "An API that provides rainfall-related data of the city of Barcelona.",
            },
            "server": {
                "host": "127.0.0.1",
                "port": 8000,
                "reload": True,
            },
        }

        """

        return APISettings(**self.yaml_config["api"])

    @cached_property
    def get_webapp_server_settings(self) -> WebappServerSettings:
        """
        Return Flask server settings.

        Example:
        {
            "host": "127.0.0.1",
            "port": 5000,
            "debug": True,
        }
        """

        return WebappServerSettings(**self.yaml_config["webapp"])
