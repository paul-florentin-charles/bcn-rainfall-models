"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from yaml import safe_load

CONFIG_FILE_PATH: str = './config.yaml'
UTF_8: str = 'utf-8'
MODE: str = 'rt'


def get_dataset_url() -> str:
    """
    Build the dataset URL location from the configuration.

    :return: The dataset URL as a String.
    """
    dataset_url: str = ""
    with open(CONFIG_FILE_PATH, mode=MODE, encoding=UTF_8) as stream:
        yaml_config: dict = safe_load(stream)
        dataset_url += yaml_config['base_url']

        yaml_dataset_config: dict = yaml_config['dataset']
        dataset_url += f"/dataset/{yaml_dataset_config['id']}"
        dataset_url += f"/resource/{yaml_dataset_config['resource_id']}"
        dataset_url += f"/download/{yaml_dataset_config['file_name']}"

    return dataset_url


def get_start_year() -> int:
    """
    Retrieve the year the data should start at.

    :return: A year as an Integer.
    """
    start_year: int = 0
    with open(CONFIG_FILE_PATH, mode=MODE, encoding=UTF_8) as stream:
        yaml_config: dict = safe_load(stream)
        start_year += yaml_config['data']['start_year']

    return start_year


def get_round_precision() -> int:
    """
    The decimal precision of Rainfall values.

    :return: A rounding precision as an Integer.
    """
    rounding_precision: int = 0
    with open(CONFIG_FILE_PATH, mode=MODE, encoding=UTF_8) as stream:
        yaml_config: dict = safe_load(stream)
        rounding_precision += yaml_config['data']['round_precision']

    return rounding_precision
