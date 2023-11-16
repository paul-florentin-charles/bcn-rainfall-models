#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring

"""
Run the Flask app from this file.
Currently developing the Swagger API using flasgger.
"""

from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, Response

from src.api.utils import parse_args
from src.config import Config
import src.api.schemas as sch
from src.api.swagger.rainfall import (average_specs, normal_specs,
                                      relative_distance_to_normal_specs,
                                      standard_deviation_specs)
from src.api.swagger.year import below_normal_specs, above_normal_specs
import src.api.swagger.parameters_specs as param
from src.core.models.all_rainfall import AllRainfall
from src.core.utils.enums.time_modes import TimeMode

cfg = Config()
all_rainfall = AllRainfall(cfg.get_dataset_url(),
                           cfg.get_start_year(),
                           cfg.get_rainfall_precision())

app = Flask(__name__)
swagger = Swagger(app, template_file=f"{cfg.get_api_doc_path()}/template.yaml")


@app.route(f"{swagger.template['basePath']}/rainfall/average")
@swag_from(average_specs.route_specs)
def average_rainfall() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.begin_year,
                               param.end_year,
                               param.month,
                               param.season)

    to_return: dict = {
        'name': 'average rainfall (mm)',
        'value': all_rainfall.get_average_rainfall(params[0], *params[1:]),
        'begin_year': params[1],
        'end_year': params[2] if params[2] is not None else all_rainfall.get_last_year(),
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[3]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[4]

    return jsonify(sch.RainfallSchema().load(to_return))


@app.route(f"{swagger.template['basePath']}/rainfall/normal")
@swag_from(normal_specs.route_specs)
def normal_rainfall() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.begin_year,
                               param.month,
                               param.season)

    to_return: dict = {
        'name': 'rainfall normal (mm)',
        'value': all_rainfall.get_normal(params[0], params[1], *params[2:]),
        'begin_year': params[1],
        'end_year': params[1] + 29,
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[2]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[3]

    return jsonify(sch.RainfallSchema().load(to_return))


@app.route(f"{swagger.template['basePath']}/rainfall/relative_distance_to_normal")
@swag_from(relative_distance_to_normal_specs.route_specs)
def rainfall_relative_distance_to_normal() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.normal_year,
                               param.begin_year,
                               param.end_year,
                               param.month,
                               param.season)

    to_return: dict = {
        'name': 'relative distance to rainfall normal (%)',
        'value': all_rainfall.get_relative_distance_from_normal(
            params[0], params[1], params[2], *params[3:]
        ),
        'normal_year': params[1],
        'begin_year': params[2],
        'end_year': params[3] if params[3] is not None else all_rainfall.get_last_year(),
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[4]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[5]

    return jsonify(sch.RelativeDistanceToRainfallNormalSchema().load(to_return))


@app.route(f"{swagger.template['basePath']}/rainfall/standard_deviation")
@swag_from(standard_deviation_specs.route_specs)
def rainfall_standard_deviation() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.begin_year,
                               param.end_year,
                               param.month,
                               param.season)

    to_return: dict = {
        'name': 'rainfall standard deviation (mm)',
        'value': all_rainfall.get_rainfall_standard_deviation(params[0], params[1], *params[2:]),
        'begin_year': params[1],
        'end_year': params[2] if params[2] is not None else all_rainfall.get_last_year(),
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[3]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[4]

    return jsonify(sch.RainfallSchema().load(to_return))


@app.route(f"{swagger.template['basePath']}/year/below_normal")
@swag_from(below_normal_specs.route_specs)
def years_below_normal() -> Response:
    normal_year: int = request.args.get(param.normal_year['name'],
                                        default=param.normal_year['default'],
                                        type=int)
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    end_year: int = request.args.get(param.end_year['name'],
                                     default=param.end_year['default'],
                                     type=int)
    value: float = all_rainfall.yearly_rainfall.get_years_below_normal(
        normal_year,
        begin_year,
        end_year
    )

    return jsonify(sch.YearsBelowNormalSchema().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": end_year,
    }))


@app.route(f"{swagger.template['basePath']}/year/above_normal")
@swag_from(above_normal_specs.route_specs)
def years_above_normal() -> Response:
    normal_year: int = request.args.get(param.normal_year['name'],
                                        default=param.normal_year['default'],
                                        type=int)
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    end_year: int = request.args.get(param.end_year['name'],
                                     default=param.end_year['default'],
                                     type=int)
    value: float = all_rainfall.yearly_rainfall.get_years_above_normal(
        normal_year,
        begin_year,
        end_year
    )

    return jsonify(sch.YearsAboveNormalSchema().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": end_year,
    }))


if __name__ == '__main__':
    app.run(debug=True)
