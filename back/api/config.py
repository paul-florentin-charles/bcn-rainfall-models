"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

import os
from functools import cached_property
from typing import Optional

from pydantic import BaseModel, Field

from base_config import BaseConfig


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


class Config(BaseConfig):
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance: Optional["Config"] = None

    def __new__(cls, path=os.path.join("back", "api", "config.yml")):
        return super().__new__(cls, path=path)

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
