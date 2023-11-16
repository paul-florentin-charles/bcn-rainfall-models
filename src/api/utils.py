"""
Collection of utility functions for API purposes.
"""

from typing import Union

from werkzeug.datastructures.structures import MultiDict


def parse_args(args: MultiDict[str, str], *params: dict) -> tuple:
    """
    Parse Flask query arguments into a tuple.

    :param args: Flask request args as a MultiDict.
    :param params: Desired parameters to parse as a list of swagger-conformed dicts.
    :return: Tuple containing retrieved values from query parameters.
    """
    to_return: list = []
    for param in params:
        to_return.append(
            args.get(param['name'],
                     default=param['default'],
                     type=swagger_type_to_python_type(param['type']))
        )

    return tuple(to_return)


def swagger_type_to_python_type(swagger_type: str) -> Union[type, None]:
    """
    Convert a Swagger known type into a Python type.

    :param swagger_type: Swagger type as a string.
    :return: Python type if recognized. None otherwise.
    """
    python_type = None
    if swagger_type == 'integer':
        python_type = int
    elif swagger_type == 'number':
        python_type = float
    elif swagger_type == 'string':
        python_type = str

    return python_type
