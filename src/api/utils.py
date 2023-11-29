"""
Collection of utility functions for API purposes.
"""
from http import HTTPStatus
from typing import Union, Optional

from flask import make_response, jsonify, Response
from werkzeug.datastructures.structures import MultiDict

from src.api.error_wrappers import bad_request
from src.core.utils.enums.time_modes import TimeMode


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
            args.get(
                param["name"],
                default=param["default"],
                type=swagger_type_to_python_type(param["type"]),
            )
        )

    return tuple(to_return)


def swagger_type_to_python_type(swagger_type: str) -> Union[type, None]:
    """
    Convert a Swagger known type into a Python type.

    :param swagger_type: Swagger type as a string.
    :return: Python type if recognized. None otherwise.
    """
    python_type = None
    if swagger_type == "integer":
        python_type = int
    elif swagger_type == "number":
        python_type = float
    elif swagger_type == "string":
        python_type = str

    return python_type


def manage_time_mode_errors(
    response_dict: dict, time_mode: str, month: Optional[str], season: Optional[str]
) -> Union[Response, dict]:
    """
    Manage errors related to time mode issues.
    If time mode is set to monthly and month is None.
    If time mode is set to seasonal and season is None.

    :param response_dict: Dict where to store response fields.
    :param time_mode: A string setting the time period ['yearly', 'monthly', 'seasonal']
    :param month: A string corresponding to the month name.
    Set if time_mode is 'monthly' (optional)
    :param season: A string corresponding to the season name.
    Possible values are within ['WINTER', 'SPRING', 'SUMMER', 'FALL'].
    Set if time_mode is 'seasonal' (optional)
    :return: Either a Flask Response if there is an error or the updated dictionary.
    """
    if time_mode == TimeMode.MONTHLY.value:
        if month is None:
            return bad_request("Month cannot be null.")

        response_dict["month"] = month.lower()

    if time_mode == TimeMode.SEASONAL.value:
        if season is None:
            return bad_request("Season cannot be null.")

        response_dict["season"] = season.lower()

    return response_dict
