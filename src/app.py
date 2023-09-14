#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring

"""
Run the Flask app from this file.
Currently developing the Swagger API using flasgger.
"""

from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, Response

from api.parameters import Parameter
from core.models.all_rainfall import AllRainfall
from config import Config

cfg = Config()
all_rainfall = AllRainfall(cfg.get_dataset_url(),
                           cfg.get_start_year(),
                           cfg.get_rainfall_precision())

app = Flask(__name__)
swagger = Swagger(app, template_file=f"{cfg.get_api_doc_path()}/template.yaml")


@app.route('/api/rainfall/average')
@swag_from(f"{cfg.get_api_doc_path()}/rainfall/average.yaml")
def average_rainfall() -> Response:
    return jsonify(all_rainfall.yearly_rainfall.get_average_yearly_rainfall(
        begin_year=request.args.get(*Parameter.BEGIN_YEAR.value),
        end_year=request.args.get(*Parameter.END_YEAR.value)
    ))


@app.route('/api/rainfall/normal')
@swag_from(f"{cfg.get_api_doc_path()}/rainfall/normal.yaml")
def normal_rainfall() -> Response:
    return jsonify(all_rainfall.yearly_rainfall.get_normal(
        begin_year=request.args.get(*Parameter.BEGIN_YEAR.value))
    )


@app.route('/api/rainfall/relative_distance_to_normal')
@swag_from(f"{cfg.get_api_doc_path()}/rainfall/relative_distance_to_normal.yaml")
def rainfall_relative_distance_to_normal() -> Response:
    return jsonify(all_rainfall.yearly_rainfall.get_relative_distance_from_normal(
        normal=request.args.get(*Parameter.NORMAL.value),
        begin_year=request.args.get(*Parameter.BEGIN_YEAR.value),
        end_year=request.args.get(*Parameter.END_YEAR.value)
    ))


@app.route('/api/rainfall/standard_deviation')
@swag_from(f"{cfg.get_api_doc_path()}/rainfall/standard_deviation.yaml")
def standard_deviation() -> Response:
    return jsonify(all_rainfall.yearly_rainfall.get_standard_deviation(
        begin_year=request.args.get(*Parameter.BEGIN_YEAR.value),
        end_year=request.args.get(*Parameter.END_YEAR.value)
    ))


@app.route('/api/year/below_normal')
@swag_from(f"{cfg.get_api_doc_path()}/year/below_normal.yaml")
def years_below_normal() -> Response:
    return jsonify(all_rainfall.yearly_rainfall.get_years_below_normal(
        normal=request.args.get(*Parameter.NORMAL.value),
        begin_year=request.args.get(*Parameter.BEGIN_YEAR.value),
        end_year=request.args.get(*Parameter.END_YEAR.value)
    ))


@app.route('/api/year/above_normal')
@swag_from(f"{cfg.get_api_doc_path()}/year/above_normal.yaml")
def years_above_normal() -> Response:
    return jsonify(all_rainfall.yearly_rainfall.get_years_above_normal(
        normal=request.args.get(*Parameter.NORMAL.value),
        begin_year=request.args.get(*Parameter.BEGIN_YEAR.value),
        end_year=request.args.get(*Parameter.END_YEAR.value)
    ))


if __name__ == '__main__':
    app.run(debug=True)
