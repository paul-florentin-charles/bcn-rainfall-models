"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

import os.path
from functools import cached_property
from typing import Optional

from pydantic import BaseModel, Field

from base_config import BaseConfig


class WebappServerSettings(BaseModel):
    """Type definition for Flask server settings."""

    host: str
    port: int
    debug: bool | None = Field(None)


class Config(BaseConfig):
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance: Optional["Config"] = None

    def __new__(cls, path=os.path.join("webapp", "config.yml")):
        return super().__new__(cls, path=path)

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
