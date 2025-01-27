"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from typing import Any

from yaml import safe_load, parser  # type: ignore


class Config:
    """
    Provides function to retrieve and/or build fields from YAML Configuration.
    It needs to be instantiated first to be loaded.
    """

    def __init__(self, path="config.yml"):
        self.path = path
        try:
            with open(self.path, mode="rt", encoding="utf-8") as stream:
                self.yaml_config: dict = safe_load(stream)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f'Configuration file not found at "{self.path}"'
            ) from exc
        except parser.ParserError as exc:
            raise parser.ParserError(
                f'Configuration file at "{self.path}" cannot be parsed: not a valid YAML file!'
            ) from exc

    def get_dataset_url(self) -> str:
        """
        Build the dataset URL location from the configuration.

        :return: The dataset URL as a String.
        """

        return self.yaml_config["dataset"]["file_url"]

    def get_dataset_path(self) -> str:
        """
        Return the path to the local copy of the dataset.

        :return: The dataset path as a string.
        """

        return self.yaml_config["dataset"]["local_file_path"]

    def get_start_year(self) -> int:
        """
        Retrieve the year the data should start at.

        :return: A year as an Integer.
        """

        return self.yaml_config["data"]["start_year"]

    def get_rainfall_precision(self) -> int:
        """
        The decimal precision of Rainfall values.

        :return: A rounding precision as an Integer.
        """

        return self.yaml_config["data"]["rainfall_precision"]

    def get_kmeans_clusters(self) -> int:
        """
        The number of clusters to use for K-Means clustering of Rainfall data.

        :return: A number of clusters as an Integer.
        """

        return self.yaml_config["data"]["kmeans_clusters"]

    def get_api_server_settings(self) -> dict[str, Any]:
        """
        Return Uvicorn server settings to run FastAPI app.

        ex:
        {
            "host": "127.0.0.1",
            "port": 8000,
        }
        """

        return self.yaml_config["api"]["server"]

    def get_fastapi_settings(self) -> dict[str, Any]:
        """
        Return FastAPI settings to initiate app.

        ex:
        {
            "debug": True,
            "root_path": "/api",
            "title": "Barcelona Rainfall API",
            "summary": "An API that provides rainfall-related data of the city of Barcelona."
        }
        """

        return self.yaml_config["api"]["fastapi"]

    def get_webapp_server_settings(self) -> dict[str, Any]:
        """
        Return Flask server settings.

        ex:
        {
            "host": "127.0.0.1",
            "port": 5000
        }
        """

        return self.yaml_config["webapp"]
