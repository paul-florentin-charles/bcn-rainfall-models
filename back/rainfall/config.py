"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

import os
from functools import cached_property
from typing import Optional

from pydantic import BaseModel, Field

from base_config import BaseConfig


class DataSettings(BaseModel):
    """Type definition for data settings."""

    file_url: str
    local_file_path: str | None = Field(None)
    start_year: int
    rainfall_precision: int
    kmeans_clusters: int | None = Field(None)


class Config(BaseConfig):
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance: Optional["Config"] = None

    def __new__(cls, path=os.path.join("back", "rainfall", "config.yml")):
        return super().__new__(cls, path=path)

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
