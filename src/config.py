from yaml import safe_load

CONFIG_YAML: str = 'config.yaml'


def get_dataset_url() -> str:
    dataset_url: str = ""
    with open(CONFIG_YAML, 'r') as stream:
        yaml_config: dict = safe_load(stream)
        dataset_url += yaml_config['base_url']

        yaml_dataset_config: dict = yaml_config['dataset']
        dataset_url += f"/dataset/{yaml_dataset_config['id']}"
        dataset_url += f"/resource/{yaml_dataset_config['resource_id']}"
        dataset_url += f"/download/{yaml_dataset_config['file_name']}"

    return dataset_url


def get_start_year() -> int:
    start_year: int = 0
    with open(CONFIG_YAML, 'r') as stream:
        yaml_config: dict = safe_load(stream)
        start_year += yaml_config['data']['start_year']

    return start_year


def get_rounding_precision() -> int:
    rounding_precision: int = 0
    with open(CONFIG_YAML, 'r') as stream:
        yaml_config: dict = safe_load(stream)
        rounding_precision += yaml_config['data']['rounding_precision']

    return rounding_precision
