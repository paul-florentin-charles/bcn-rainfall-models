"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""
from typing import Optional

from yaml import safe_load

CONFIG_FILE_PATH: str = 'config.yaml'
UTF_8: str = 'utf-8'
MODE: str = 'rt'


class Config:
    """
    Provides function to retrieve and/or build fields from YAML Configuration.

    It needs to be instantiated first to be loaded.
    """

    def __init__(self, config_file_path: Optional[str] = None):
        self.config_file_path: str = CONFIG_FILE_PATH \
            if config_file_path is None \
            else config_file_path
        with open(self.config_file_path, mode=MODE, encoding=UTF_8) as stream:
            self.yaml_config: dict = safe_load(stream)

    def get_dataset_url(self) -> str:
        """
        Build the dataset URL location from the configuration.

        :return: The dataset URL as a String.
        """
        dataset_url: str = self.yaml_config['base_url']

        yaml_dataset_config: dict = self.yaml_config['dataset']
        dataset_url += f"/dataset/{yaml_dataset_config['id']}"
        dataset_url += f"/resource/{yaml_dataset_config['resource_id']}"
        dataset_url += f"/download/{yaml_dataset_config['file_name']}"

        return dataset_url

    def get_start_year(self) -> int:
        """
        Retrieve the year the data should start at.

        :return: A year as an Integer.
        """

        return self.yaml_config['data']['start_year']

    def get_rainfall_precision(self) -> int:
        """
        The decimal precision of Rainfall values.

        :return: A rounding precision as an Integer.
        """

        return self.yaml_config['data']['rainfall_precision']

    def get_kmeans_clusters(self) -> int:
        """
        The number of clusters to use for K-Means clustering of Rainfall data.

        :return: A number of clusters as an Integer.
        """

        return self.yaml_config['data']['kmeans_clusters']
