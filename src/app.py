#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring,no-value-for-parameter

"""
Run the Flask app from this file.
Currently developing the Swagger API using flasgger.
"""

from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, Response, send_file

import src.api.schemas as sch
import src.api.swagger.parameters_specs as param
from src.api.swagger.csv import minimal_csv_specs
from src.api.swagger.rainfall import (average_specs, normal_specs,
                                      relative_distance_to_normal_specs,
                                      standard_deviation_specs)
from src.api.swagger.year import below_normal_specs, above_normal_specs
from src.api.utils import parse_args
from src.config import Config
from src.core.models.all_rainfall import AllRainfall
from src.core.utils.enums.time_modes import TimeMode

cfg = Config()
all_rainfall = AllRainfall(cfg.get_dataset_url(),
                           cfg.get_start_year(),
                           cfg.get_rainfall_precision())

app = Flask(__name__)
swagger = Swagger(app, template_file=f"{cfg.get_api_doc_path()}/template.yaml")
base_path: str = swagger.template['basePath']


@app.route(f"{base_path}/rainfall/average")
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
        'value': all_rainfall.get_average_rainfall(*params),
        'begin_year': params[1],
        'end_year': params[2] if params[2] is not None else all_rainfall.get_last_year(),
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[3]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[4]

    return jsonify(sch.RainfallSchema().load(to_return))


@app.route(f"{base_path}/rainfall/normal")
@swag_from(normal_specs.route_specs)
def normal_rainfall() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.begin_year,
                               param.month,
                               param.season)

    to_return: dict = {
        'name': 'rainfall normal (mm)',
        'value': all_rainfall.get_normal(*params),
        'begin_year': params[1],
        'end_year': params[1] + 29,
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[2]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[3]

    return jsonify(sch.RainfallSchema().load(to_return))


@app.route(f"{base_path}/rainfall/relative_distance_to_normal")
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
        'value': all_rainfall.get_relative_distance_from_normal(*params),
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


@app.route(f"{base_path}/rainfall/standard_deviation")
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
        'value': all_rainfall.get_rainfall_standard_deviation(*params),
        'begin_year': params[1],
        'end_year': params[2] if params[2] is not None else all_rainfall.get_last_year(),
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[3]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[4]

    return jsonify(sch.RainfallSchema().load(to_return))


@app.route(f"{base_path}/year/below_normal")
@swag_from(below_normal_specs.route_specs)
def years_below_normal() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.normal_year,
                               param.begin_year,
                               param.end_year,
                               param.month,
                               param.season)

    to_return: dict = {
        'name': 'years below rainfall normal',
        'value': all_rainfall.get_years_below_normal(*params),
        'normal_year': params[1],
        'begin_year': params[2],
        'end_year': params[3] if params[3] is not None else all_rainfall.get_last_year(),
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[4]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[5]

    return jsonify(sch.YearsAboveOrBelowNormalSchema().load(to_return))


@app.route(f"{base_path}/year/above_normal")
@swag_from(above_normal_specs.route_specs)
def years_above_normal() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.normal_year,
                               param.begin_year,
                               param.end_year,
                               param.month,
                               param.season)

    to_return: dict = {
        'name': 'years above rainfall normal',
        'value': all_rainfall.get_years_above_normal(*params),
        'normal_year': params[1],
        'begin_year': params[2],
        'end_year': params[3] if params[3] is not None else all_rainfall.get_last_year(),
        'time_mode': params[0]
    }

    if params[0] == TimeMode.MONTHLY.value:
        to_return['month'] = params[4]

    if params[0] == TimeMode.SEASONAL.value:
        to_return['season'] = params[5]

    return jsonify(sch.YearsAboveOrBelowNormalSchema().load(to_return))


@app.route(f"{base_path}/csv/minimal_csv")
@swag_from(minimal_csv_specs.route_specs)
def minimal_csv() -> Response:
    params: tuple = parse_args(request.args,
                               param.time_mode,
                               param.month,
                               param.season,
                               param.csv_path)

    all_rainfall.export_as_csv(*params)

    return send_file(params[-1], mimetype="text/csv", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
