#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run the Flask app from this file.
Currently developing the Swagger API using flasgger.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, Response, send_file

import src.api.swagger.parameters_specs as param
from src.api.schemas import (
    RainfallSchema,
    RelativeDistanceToRainfallNormalSchema,
    YearsAboveOrBelowNormalSchema,
)
from src.api.swagger.csv import minimal_csv_specs
from src.api.swagger.graph import monthly_averages_specs, seasonal_averages_specs
from src.api.swagger.media_types import MediaType
from src.api.swagger.rainfall import (
    average_specs,
    normal_specs,
    relative_distance_to_normal_specs,
    standard_deviation_specs,
)
from src.api.swagger.year import below_normal_specs, above_normal_specs
from src.api.utils import parse_args, manage_time_mode_errors
from src.config import Config
from src.core.models.all_rainfall import AllRainfall
from src.core.utils.enums.time_modes import TimeMode

cfg = Config()
all_rainfall = AllRainfall(
    cfg.get_dataset_url(), cfg.get_start_year(), cfg.get_rainfall_precision()
)

app = Flask(__name__)
swagger = Swagger(app, template_file=f"{cfg.get_api_doc_path()}/template.yaml")
base_path: str = swagger.template["basePath"]


@app.route(f"{base_path}/rainfall/average")
@swag_from(average_specs.route_specs)
def average_rainfall() -> Response:
    params = parse_args(
        request.args,
        param.time_mode,
        param.begin_year,
        param.end_year,
        param.month,
        param.season,
    )

    to_return = manage_time_mode_errors({}, params[0], params[3], params[4])
    if isinstance(to_return, Response):
        return to_return

    to_return.update(
        {
            "name": "average rainfall (mm)",
            "value": all_rainfall.get_average_rainfall(*params),
            "begin_year": params[1],
            "end_year": params[2] or all_rainfall.get_last_year(),
            "time_mode": TimeMode[params[0]],
        }
    )

    return jsonify(RainfallSchema().dump(to_return))


@app.route(f"{base_path}/rainfall/normal")
@swag_from(normal_specs.route_specs)
def normal_rainfall() -> Response:
    params = parse_args(
        request.args, param.time_mode, param.begin_year, param.month, param.season
    )

    to_return = manage_time_mode_errors({}, params[0], params[2], params[3])
    if isinstance(to_return, Response):
        return to_return

    to_return.update(
        {
            "name": "rainfall normal (mm)",
            "value": all_rainfall.get_normal(*params),
            "begin_year": params[1],
            "end_year": params[1] + 29,
            "time_mode": TimeMode[params[0]],
        }
    )

    return jsonify(RainfallSchema().dump(to_return))


@app.route(f"{base_path}/rainfall/relative_distance_to_normal")
@swag_from(relative_distance_to_normal_specs.route_specs)
def rainfall_relative_distance_to_normal() -> Response:
    params = parse_args(
        request.args,
        param.time_mode,
        param.normal_year,
        param.begin_year,
        param.end_year,
        param.month,
        param.season,
    )

    to_return = manage_time_mode_errors({}, params[0], params[4], params[5])
    if isinstance(to_return, Response):
        return to_return

    to_return.update(
        {
            "name": "relative distance to rainfall normal (%)",
            "value": all_rainfall.get_relative_distance_from_normal(*params),
            "normal_year": params[1],
            "begin_year": params[2],
            "end_year": params[3] or all_rainfall.get_last_year(),
            "time_mode": TimeMode[params[0]],
        }
    )

    return jsonify(RelativeDistanceToRainfallNormalSchema().dump(to_return))


@app.route(f"{base_path}/rainfall/standard_deviation")
@swag_from(standard_deviation_specs.route_specs)
def rainfall_standard_deviation() -> Response:
    params = parse_args(
        request.args,
        param.time_mode,
        param.begin_year,
        param.end_year,
        param.month,
        param.season,
    )

    to_return = manage_time_mode_errors({}, params[0], params[3], params[4])
    if isinstance(to_return, Response):
        return to_return

    to_return.update(
        {
            "name": "rainfall standard deviation (mm)",
            "value": all_rainfall.get_rainfall_standard_deviation(*params),
            "begin_year": params[1],
            "end_year": params[2] or all_rainfall.get_last_year(),
            "time_mode": TimeMode[params[0]],
        }
    )

    return jsonify(RainfallSchema().dump(to_return))


@app.route(f"{base_path}/year/below_normal")
@swag_from(below_normal_specs.route_specs)
def years_below_normal() -> Response:
    params = parse_args(
        request.args,
        param.time_mode,
        param.normal_year,
        param.begin_year,
        param.end_year,
        param.month,
        param.season,
    )

    to_return = manage_time_mode_errors({}, params[0], params[4], params[5])
    if isinstance(to_return, Response):
        return to_return

    to_return.update(
        {
            "name": "years below rainfall normal",
            "value": all_rainfall.get_years_below_normal(*params),
            "normal_year": params[1],
            "begin_year": params[2],
            "end_year": params[3] or all_rainfall.get_last_year(),
            "time_mode": TimeMode[params[0]],
        }
    )

    return jsonify(YearsAboveOrBelowNormalSchema().dump(to_return))


@app.route(f"{base_path}/year/above_normal")
@swag_from(above_normal_specs.route_specs)
def years_above_normal() -> Response:
    params = parse_args(
        request.args,
        param.time_mode,
        param.normal_year,
        param.begin_year,
        param.end_year,
        param.month,
        param.season,
    )

    to_return = manage_time_mode_errors({}, params[0], params[4], params[5])
    if isinstance(to_return, Response):
        return to_return

    to_return.update(
        {
            "name": "years above rainfall normal",
            "value": all_rainfall.get_years_above_normal(*params),
            "normal_year": params[1],
            "begin_year": params[2],
            "end_year": params[3] or all_rainfall.get_last_year(),
            "time_mode": TimeMode[params[0]],
        }
    )

    return jsonify(YearsAboveOrBelowNormalSchema().dump(to_return))


@app.route(f"{base_path}/csv/minimal_csv")
@swag_from(minimal_csv_specs.route_specs)
def minimal_csv() -> Response:
    params = parse_args(
        request.args, param.time_mode, param.month, param.season, param.file_name
    )

    error = manage_time_mode_errors({}, params[0], params[1], params[2])
    if isinstance(error, Response):
        return error

    all_rainfall.export_as_csv(*params)

    return send_file(params[-1], mimetype=MediaType.TXT_CSV, as_attachment=True)


@app.route(f"{base_path}/graph/monthly_averages")
@swag_from(monthly_averages_specs.route_specs)
def monthly_averages() -> Response:
    params = parse_args(request.args, param.file_name, param.begin_year, param.end_year)

    all_rainfall.bar_rainfall_averages(begin_year=params[1], end_year=params[2])
    plt.savefig(params[0], format="svg")
    plt.close()

    return send_file(params[0], mimetype=MediaType.IMG_SVG, as_attachment=True)


@app.route(f"{base_path}/graph/seasonal_averages")
@swag_from(seasonal_averages_specs.route_specs)
def seasonal_averages() -> Response:
    params = parse_args(request.args, param.file_name, param.begin_year, param.end_year)

    all_rainfall.bar_rainfall_averages(
        monthly=False, begin_year=params[1], end_year=params[2]
    )
    plt.savefig(params[0], format="svg")
    plt.close()

    return send_file(params[0], mimetype=MediaType.IMG_SVG, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
