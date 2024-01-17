"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from yaml import safe_load, parser  # type: ignore

CONFIG_FNAME: str = "config.yaml"


class Config:
    """
    Provides function to retrieve and/or build fields from YAML Configuration.

    It needs to be instantiated first to be loaded.
    """

    def __init__(self, path=CONFIG_FNAME):
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
        dataset_url: str = self.yaml_config["base_url"]

        yaml_dataset_config: dict = self.yaml_config["dataset"]
        dataset_url += f"/dataset/{yaml_dataset_config['id']}"
        dataset_url += f"/resource/{yaml_dataset_config['resource_id']}"
        dataset_url += f"/download/{yaml_dataset_config['file_name']}"

        return dataset_url

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

    def get_api_doc_path(self) -> str:
        """
        The path to Swagger YAML spec files to document API.

        :return: The path to API Swagger documentation as a String
        """

        return self.yaml_config["api"]["doc_path"]
