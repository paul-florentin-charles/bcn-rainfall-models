"""
Provides functions parsing the YAML Configuration file to retrieve parameters.
"""

from typing import Optional

from api_session import JSONDict
from yaml import parser, safe_load  # type: ignore


class BaseConfig:
    """
    Provides function to retrieve fields from YAML configuration.
    It needs to be instantiated first to be loaded.
    Configuration is cached but can be reloaded if needed.
    """

    _instance: Optional["BaseConfig"] = None
    path: str
    yaml_config: JSONDict

    def __new__(cls, *, path: str):
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
